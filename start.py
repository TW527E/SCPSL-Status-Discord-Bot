from __future__ import annotations

import asyncio
import inspect
import json
import os
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import discord
import requests
from discord import app_commands
from discord.ext import commands

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python 3.8 以下沒有 zoneinfo，保留 UTC+8 後備。
    ZoneInfo = None


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "setting.json"
DATA_DIR = BASE_DIR / "data"
ENV_FILE = BASE_DIR / ".env"

FIELD_GROUPS = (
    "Status",
    "Port",
    "Players",
    "Version",
    "Pastebin",
    "Infomation",  # 保留原本設定檔拼字，避免既有 data/*.json 失效。
    "LastOnline",
)


def read_json(path: Path) -> dict[str, Any]:
    """讀取 JSON 檔案，所有設定與狀態資料都走同一個入口。"""
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """用暫存檔替換，避免寫入中斷時留下半個 JSON。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=4)
        file.write("\n")
    os.replace(tmp_path, path)


def load_environment(path: Path = ENV_FILE) -> None:
    """載入 .env；有安裝 python-dotenv 時優先使用，沒有也能基本解析。"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None

    if load_dotenv:
        load_dotenv(path)
        return

    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"缺少環境變數 {name}，請在 .env 補上。")
    return value


def now_in_config_timezone(config: dict[str, Any]) -> datetime:
    tz_name = config.get("timezone", "Asia/Taipei")
    if ZoneInfo is not None:
        try:
            return datetime.now(ZoneInfo(tz_name))
        except Exception:
            pass
    return datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))


def render_template(template: Any, values: dict[str, Any]) -> str:
    """替換設定檔中的 %Token%，並修正原設定為避免跳脫而使用的全形字元。"""
    text = str(template)
    for key, value in values.items():
        text = text.replace(f"%{key}%", str(value))
    return text.replace("＼｜／", "\\|/")


def parse_player_count(players: Any) -> int:
    """SCPSL API 常回傳 0/30 這類字串，只取目前人數判斷機器人狀態。"""
    first_part = str(players).split("/", 1)[0].strip()
    try:
        return int(first_part)
    except ValueError:
        return 0


def get_avatar_url(user: discord.abc.User | None) -> str | None:
    if user is None:
        return None
    display_avatar = getattr(user, "display_avatar", None)
    if display_avatar is not None:
        return str(display_avatar.url)
    avatar_url = getattr(user, "avatar_url", None)
    return str(avatar_url) if avatar_url else None


def create_intents() -> discord.Intents:
    """Slash command 不需要 Message Content Intent，只保留狀態更新會用到的基本 intent。"""
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    return intents


@dataclass
class BotRuntime:
    key: str
    name: str
    token_env: str
    token: str
    data_path: Path
    sync_guild_ids: list[int]
    bot: commands.Bot
    ready_logged: bool = False
    commands_synced: bool = False

    def load_data(self) -> dict[str, Any]:
        return read_json(self.data_path)

    def save_data(self, data: dict[str, Any]) -> None:
        write_json(self.data_path, data)


async def is_bot_owner(interaction: discord.Interaction) -> bool:
    """限制 slash command 只有 bot owner 可以使用。"""
    client = interaction.client
    if isinstance(client, commands.Bot):
        return await client.is_owner(interaction.user)
    return False


class ServerControlCog(commands.Cog):
    """每台 bot 共用的管理指令。"""

    def __init__(self, runtime: BotRuntime):
        self.runtime = runtime

    @app_commands.command(name="here", description="在目前頻道建立或更新伺服器狀態訊息")
    @app_commands.check(is_bot_owner)
    async def here(self, interaction: discord.Interaction) -> None:
        """Slash command：建立狀態訊息，並把訊息位置寫回 data/server_*.json。"""
        if interaction.guild is None or interaction.channel is None:
            await interaction.response.send_message("這個指令只能在伺服器頻道中使用。", ephemeral=True)
            return

        if not hasattr(interaction.channel, "send"):
            await interaction.response.send_message("目前頻道無法發送狀態訊息。", ephemeral=True)
            return

        print(f"[{self.runtime.name}] {interaction.user} 使用 /here 指令")
        await interaction.response.defer(ephemeral=True, thinking=True)

        message = await interaction.channel.send("等等，等我一下")
        data = self.runtime.load_data()
        data["message"] = {
            "guild_id": interaction.guild.id,
            "channel_id": message.channel.id,
            "message_id": message.id,
        }
        self.runtime.save_data(data)
        print(f"[{self.runtime.name}] 已更新狀態訊息位置到 {self.runtime.data_path.name}")
        await interaction.followup.send(
            f"已更新 `{self.runtime.data_path.name}` 的狀態訊息位置。",
            ephemeral=True,
        )

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.CheckFailure):
            message = "只有此 bot 的 owner 可以使用這個指令。"
        else:
            message = f"指令執行失敗：{error}"
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)


class StatusManager:
    """集中處理 SCPSL API 查詢、Embed 產生與多 bot 狀態更新。"""

    def __init__(self, config: dict[str, Any], runtimes: list[BotRuntime]):
        self.config = config
        self.runtimes = runtimes
        self.api_config = config["api"]
        self.cache_path = DATA_DIR / self.api_config.get("cache_file", "scpsl_status_cache.json")

    async def wait_until_all_ready(self) -> None:
        await asyncio.gather(*(runtime.bot.wait_until_ready() for runtime in self.runtimes))

    async def status_loop(self) -> None:
        while True:
            try:
                response = await self.fetch_status()
            except Exception as exc:
                print(f"[SCPSL API] 查詢失敗: {exc}")
                response = {"Success": False, "Error": str(exc)}
            await self.update_all_servers(response)
            sleep_seconds = self.next_delay(response)
            await asyncio.sleep(sleep_seconds)

    async def fetch_status(self) -> dict[str, Any]:
        token = require_env(self.api_config["token_env"])
        account_id = require_env(self.api_config["account_id_env"])
        response = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: requests.get(
                self.api_config["base_url"],
                params={
                    "key": token,
                    "id": account_id,
                    "lo": "true",
                    "players": "true",
                    "list": "true",
                    "info": "true",
                    "pastebin": "true",
                    "version": "true",
                    "flags": "true",
                    "nicknames": "true",
                    "online": "true",
                },
                timeout=20,
            ),
        )
        response.raise_for_status()
        payload = response.json()
        self.save_api_cache(payload)
        return payload

    def save_api_cache(self, response: dict[str, Any]) -> None:
        now = now_in_config_timezone(self.config).strftime("%Y-%m-%d %H:%M:%S")
        write_json(self.cache_path, {"last_update_time": now, "response": response})

    def next_delay(self, response: dict[str, Any]) -> int:
        if response.get("Success"):
            return int(response.get("Cooldown") or self.config.get("fallback_cooldown_seconds", 24))
        return int(self.config.get("fallback_cooldown_seconds", 24))

    async def update_all_servers(self, response: dict[str, Any]) -> None:
        for runtime in self.runtimes:
            try:
                await self.update_one_server(runtime, response)
            except Exception as exc:
                print(f"[{runtime.name}] 更新失敗: {exc}")

    async def update_one_server(self, runtime: BotRuntime, response: dict[str, Any]) -> None:
        data = runtime.load_data()
        message_ref = data.get("message") or {}
        if not all(message_ref.get(key) for key in ("guild_id", "channel_id", "message_id")):
            print(f"[{runtime.name}] 尚未設定狀態訊息，請在目標頻道使用 /here")
            return

        channel = self.resolve_channel(runtime.bot, message_ref)
        if channel is None:
            print(f"[{runtime.name}] 找不到頻道 {message_ref.get('channel_id')}")
            return

        message = await channel.fetch_message(int(message_ref["message_id"]))
        embed, presence, log_values = self.build_embed(runtime, data, response)
        await self.apply_presence(runtime.bot, presence)
        await message.edit(embed=embed, content="")
        self.print_update_log(runtime, log_values)

    def resolve_channel(self, bot: commands.Bot, message_ref: dict[str, Any]) -> discord.abc.Messageable | None:
        guild = bot.get_guild(int(message_ref["guild_id"]))
        if guild is not None:
            channel = guild.get_channel(int(message_ref["channel_id"]))
            if channel is not None:
                return channel
        return bot.get_channel(int(message_ref["channel_id"]))

    def build_embed(
        self,
        runtime: BotRuntime,
        data: dict[str, Any],
        response: dict[str, Any],
    ) -> tuple[discord.Embed, tuple[discord.Status, str], dict[str, Any]]:
        now = now_in_config_timezone(self.config).strftime("%Y-%m-%d %H:%M:%S")
        embed_config = data["embed"]
        presence_config = data["presence"]
        api_server = self.find_api_server(data, response)
        state, color, status_label = self.resolve_state(response, api_server)
        common_values, language_values = self.build_template_values(embed_config, api_server, state, now)

        embed = discord.Embed(
            title=str(embed_config.get("Message Title", runtime.name)),
            description=str(embed_config.get("Server Description", "")),
            color=color,
        )
        if embed_config.get("Server Icon"):
            embed.set_thumbnail(url=str(embed_config["Server Icon"]))

        for group in FIELD_GROUPS:
            self.add_embed_group(embed, embed_config, group, state, common_values, language_values)

        footer_text = render_template(embed_config.get("Last Updated", "%Time%"), common_values)
        footer_suffix = self.config.get("footer_text")
        if footer_suffix:
            footer_text = f"{footer_text} {footer_suffix}"
        footer_icon = get_avatar_url(runtime.bot.get_user(int(self.config.get("owner_id", 0))))
        if footer_icon:
            embed.set_footer(text=footer_text, icon_url=footer_icon)
        else:
            embed.set_footer(text=footer_text)

        player_count = parse_player_count(common_values.get("Players", 0))
        if state == "Started":
            discord_status = discord.Status.idle if player_count == 0 else discord.Status.online
        else:
            discord_status = discord.Status.dnd
        activity_name = render_template(presence_config.get(f"Bot Status {state}", status_label), common_values)

        log_values = {
            "status": status_label,
            "time": now,
            "port": common_values.get("Port", "Unknown"),
            "players": common_values.get("Players", "Unknown"),
            "version": common_values.get("Version", "Unknown"),
            "pastebin": common_values.get("Pastebin", "Unknown"),
            "info": " | ".join(
                str(language_values[1].get(key, "Unknown"))
                for key in ("FriendlyFire", "Whitelist", "Modded")
            ),
        }
        return embed, (discord_status, activity_name), log_values

    def find_api_server(self, data: dict[str, Any], response: dict[str, Any]) -> dict[str, Any] | None:
        if not response.get("Success"):
            return None
        servers = response.get("Servers") or []
        try:
            index = int(data.get("server_codename"))
        except (TypeError, ValueError):
            return None
        if isinstance(servers, list) and 0 <= index < len(servers):
            return servers[index]
        return None

    def resolve_state(
        self,
        response: dict[str, Any],
        api_server: dict[str, Any] | None,
    ) -> tuple[str, int, str]:
        if not response.get("Success"):
            return "Warning", 0xFF0000, "Unavailable"
        if api_server is None:
            return "Warning", 0xFF0000, "Missing"
        if api_server.get("Online"):
            return "Started", 0x28D252, "Online"
        return "Closed", 0xFF0000, "Closed"

    def build_template_values(
        self,
        embed_config: dict[str, Any],
        api_server: dict[str, Any] | None,
        state: str,
        now: str,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        api_server = api_server or {}
        common_values = {
            "Time": now,
            "Port": api_server.get("Port", "Unknown"),
            "Players": api_server.get("Players", "Unknown"),
            "Version": api_server.get("Version", "Unknown"),
            "Pastebin": api_server.get("Pastebin", "Unknown"),
            "LastOnline": api_server.get("LastOnline", "Unknown"),
        }

        if state == "Started":
            friendly_fire = self.pick_pair(embed_config, "Friendly Fire", "On" if api_server.get("FF") else "Off")
            whitelist = self.pick_pair(embed_config, "Whitelist", "On" if api_server.get("WL") else "Off")
            modded = self.pick_pair(embed_config, "Modded", "On" if api_server.get("Modded") else "Off")
        else:
            friendly_fire = self.pick_pair(embed_config, "Friendly Fire", "Warning")
            whitelist = self.pick_pair(embed_config, "Whitelist", "Warning")
            modded = self.pick_pair(embed_config, "Modded", "Warning")

        language_values = [
            {"FriendlyFire": friendly_fire[0], "Whitelist": whitelist[0], "Modded": modded[0]},
            {"FriendlyFire": friendly_fire[1], "Whitelist": whitelist[1], "Modded": modded[1]},
        ]
        return common_values, language_values

    def pick_pair(self, embed_config: dict[str, Any], key: str, suffix: str) -> list[str]:
        value = embed_config.get(f"{key} {suffix}") or ["Unknown", "Unknown"]
        return [str(value[0]), str(value[1])]

    def add_embed_group(
        self,
        embed: discord.Embed,
        embed_config: dict[str, Any],
        group: str,
        state: str,
        common_values: dict[str, Any],
        language_values: list[dict[str, Any]],
    ) -> None:
        group_config = embed_config.get(group)
        values = embed_config.get(f"{group} {state}")
        if not group_config or not values or not group_config[0]:
            return

        embed.add_field(
            name=str(embed_config.get("Separate line", "----------")),
            value=str(group_config[1]),
            inline=False,
        )
        for index in range(2):
            value_map = common_values | language_values[index]
            embed.add_field(
                name=str(group_config[index + 2]),
                value=render_template(values[index], value_map),
                inline=True,
            )

    async def apply_presence(self, bot: commands.Bot, presence: tuple[discord.Status, str]) -> None:
        status, activity_name = presence
        await bot.change_presence(
            status=status,
            activity=discord.Activity(type=discord.ActivityType.watching, name=activity_name),
        )

    def print_update_log(self, runtime: BotRuntime, values: dict[str, Any]) -> None:
        print(f"[{runtime.name}] Data is updated, server is {values['status']}")
        print(f"＝＝＝＝＝＝《 {runtime.name} 》＝＝＝＝＝＝")
        print(f"Server is {values['status']}")
        print(f"Port: {values['port']}")
        print(f"Players: {values['players']}")
        print(f"Version: {values['version']}")
        print(f"Pastebin: {values['pastebin']}")
        print(f"Info: {values['info']}")
        print(f"＝＝＝＝＝＝[ {values['time']} ]＝＝＝＝＝＝\n")


async def maybe_add_cog(bot: commands.Bot, cog: commands.Cog) -> None:
    result = bot.add_cog(cog)
    if inspect.isawaitable(result):
        await result


async def sync_application_commands(runtime: BotRuntime) -> None:
    """同步 slash commands；指定 guild 可立即生效，未指定則走全域同步。"""
    if runtime.commands_synced:
        return

    try:
        if runtime.sync_guild_ids:
            synced_count = 0
            for guild_id in runtime.sync_guild_ids:
                guild = discord.Object(id=guild_id)
                runtime.bot.tree.copy_global_to(guild=guild)
                synced = await runtime.bot.tree.sync(guild=guild)
                synced_count += len(synced)
            print(f"[{runtime.name}] 已同步 {synced_count} 個 guild slash command。")
        else:
            synced = await runtime.bot.tree.sync()
            print(f"[{runtime.name}] 已同步 {len(synced)} 個全域 slash command。")
    except Exception as exc:
        print(f"[{runtime.name}] slash command 同步失敗: {exc}")
    else:
        runtime.commands_synced = True


def register_ready_event(runtime: BotRuntime) -> None:
    @runtime.bot.event
    async def on_ready() -> None:
        await runtime.bot.change_presence(status=discord.Status.offline)
        await sync_application_commands(runtime)
        if runtime.ready_logged:
            return
        runtime.ready_logged = True
        print("＝＝＝已登入＝＝＝")
        print(f"《 {runtime.bot.user} 》上線了")
        print(f"目前在的群組有 {runtime.bot.guilds}")
        print("＝＝＝已登入＝＝＝\n")


async def build_runtimes(config: dict[str, Any]) -> list[BotRuntime]:
    runtimes: list[BotRuntime] = []
    intents = create_intents()
    for entry in config.get("bots", []):
        if not entry.get("enabled", True):
            continue
        token = require_env(entry["token_env"])
        bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
        runtime = BotRuntime(
            key=entry["key"],
            name=entry.get("name", entry["key"]),
            token_env=entry["token_env"],
            token=token,
            data_path=DATA_DIR / entry["data_file"],
            sync_guild_ids=[int(guild_id) for guild_id in entry.get("sync_guild_ids", [])],
            bot=bot,
        )
        await maybe_add_cog(bot, ServerControlCog(runtime))
        register_ready_event(runtime)
        runtimes.append(runtime)
    if not runtimes:
        raise RuntimeError("setting.json 沒有啟用任何 bot。")
    return runtimes


async def run_bots(runtimes: list[BotRuntime], manager: StatusManager) -> None:
    start_tasks = [asyncio.create_task(runtime.bot.start(runtime.token)) for runtime in runtimes]
    start_group = asyncio.gather(*start_tasks)
    ready_group = asyncio.create_task(manager.wait_until_all_ready())
    status_task: asyncio.Task | None = None

    try:
        done, _ = await asyncio.wait({start_group, ready_group}, return_when=asyncio.FIRST_COMPLETED)
        if start_group in done:
            start_group.result()
            return

        print("所有 Discord bot 已就緒，開始同步 SCPSL 狀態。")
        status_task = asyncio.create_task(manager.status_loop())
        await start_group
    finally:
        if not ready_group.done():
            ready_group.cancel()
            with suppress(asyncio.CancelledError):
                await ready_group
        if status_task is not None:
            status_task.cancel()
            with suppress(asyncio.CancelledError):
                await status_task
        for runtime in runtimes:
            if not runtime.bot.is_closed():
                await runtime.bot.close()


async def main() -> None:
    load_environment()
    config = read_json(CONFIG_FILE)
    runtimes = await build_runtimes(config)
    manager = StatusManager(config, runtimes)
    await run_bots(runtimes, manager)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("收到中斷訊號，正在關閉。")
