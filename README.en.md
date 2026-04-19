# SCPSL Status Discord Bot

[繁體中文](README.md)

This project uses the SCPSL official API to fetch server status, then uses multiple Discord bots to update each server's status message and bot presence.

## Important Notice

This project uses the SCPSL official server list API from "several years ago". This is not a general-purpose modern API example. To use it, you must already own an SCPSL server that is listed on the official server list, and you must find the API token / account data that was assigned to that server at the time.

This cleanup only turns an old private project back into a safer, more readable, and reopenable codebase. It does not guarantee that this API still applies to new servers or any current application process.

## Files

- `start.py`: Main entry point. Loads config, starts multiple Discord bots, syncs slash commands, queries the SCPSL API, and updates Discord embeds.
- `setting.json`: Local non-secret global configuration, such as timezone, API URL, bot list, and each bot's data file.
- `setting.example.json`: Example for `setting.json`. The real runtime file name is `setting.json`.
- `.env`: Local secret data, such as the SCPSL API token, account ID, and Discord bot tokens. This file should not be committed to Git.
- `.env.example`: Example for `.env`.
- `data/server_*.json`: Per-bot / per-server data, including SCPSL server codename, Discord message location, embed text, and bot presence text.
- `data/server.example.json`: Example for `data/server_*.json`.
- `data/scpsl_status_cache.json`: Cache for the latest API response. This is updated automatically while running.

## Installation

1. Install Python 3.10 or newer.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create `.env` from `.env.example`, then fill in real tokens.
4. Make sure the Discord bot invite URL includes the `applications.commands` scope, otherwise slash commands will not appear.
5. Edit the `bots` list in `setting.json`.
6. Edit or copy `data/server_*.json`.
7. Start the bot:

```powershell
python start.py
```

## Slash Command

There is currently one management command:

```text
/here
```

Purpose: creates a status message in the current channel, then writes `guild_id`, `channel_id`, and `message_id` back to the matching `data/server_*.json`.

Restriction: only the owner of that Discord bot can use it.

## setting.json Format

See `setting.example.json` for a complete example.

```json
{
  "description": "Configuration description",
  "timezone": "Asia/Taipei",
  "fallback_cooldown_seconds": 24,
  "footer_text": "Made by YourName",
  "owner_id": 123456789012345678,
  "api": {
    "base_url": "https://api.scpslgame.com/serverinfo.php",
    "token_env": "SCPSL_API_TOKEN",
    "account_id_env": "SCPSL_ACCOUNT_ID",
    "cache_file": "scpsl_status_cache.json"
  },
  "bots": [
    {
      "key": "server_1",
      "name": "Server #1",
      "token_env": "DISCORD_BOT_TOKEN_1",
      "data_file": "server_1.json",
      "sync_guild_ids": [
        123456789012345678
      ],
      "enabled": true
    }
  ]
}
```

Field notes:

- `timezone`: Timezone used for update timestamps.
- `fallback_cooldown_seconds`: Retry interval when the API fails or does not return a cooldown.
- `footer_text`: Suffix text for the embed footer.
- `owner_id`: User ID used for the footer avatar, and also useful for identifying the maintainer.
- `api.token_env`: Environment variable name in `.env` for the SCPSL API token.
- `api.account_id_env`: Environment variable name in `.env` for the SCPSL account ID.
- `bots[].key`: Internal identifier. `server_1`, `server_2`, etc. are recommended.
- `bots[].name`: Name shown in logs.
- `bots[].token_env`: Environment variable name in `.env` for the Discord bot token.
- `bots[].data_file`: Matching `data/*.json` file name.
- `bots[].sync_guild_ids`: Discord guild IDs where slash commands should be synced immediately. Use an empty array for global sync, but global Discord slash commands may take longer to appear.
- `bots[].enabled`: Whether this bot is enabled.

## data/server_*.json Format

See `data/server.example.json` for a complete example.

```json
{
  "server_codename": 0,
  "message": {
    "guild_id": 123456789012345678,
    "channel_id": 123456789012345678,
    "message_id": 123456789012345678
  },
  "embed": {
    "Server Icon": "https://example.com/server-icon.png",
    "Message Title": "Example SCPSL Server Status",
    "Server Description": "Live server status",
    "Last Updated": "Last updated %Time% (UTC+8)",
    "Separate line": "----------",
    "Status": [
      true,
      "Status",
      "狀態",
      "Status"
    ],
    "Status Started": [
      "已正常啟動",
      "Server started"
    ]
  },
  "presence": {
    "Bot Status Started": "%Players%",
    "Bot Status Closed": "伺服器已關閉",
    "Bot Status Warning": "無法獲取狀態"
  }
}
```

The `embed` section above only shows one field group. The available groups are:

- `Status`
- `Port`
- `Players`
- `Version`
- `Pastebin`
- `Infomation`
- `LastOnline`

Every field group uses the same structure:

```json
"Status": [
  true,
  "Section title",
  "Left column field name",
  "Right column field name"
],
"Status Started": [
  "Left column value when the server is online",
  "Right column value when the server is online"
],
"Status Closed": [
  "Left column value when the server is offline",
  "Right column value when the server is offline"
],
"Status Warning": [
  "Left column value when the API fails",
  "Right column value when the API fails"
]
```

The first array value is `true` or `false`, which controls whether that field group is displayed.

Available template variables:

- `%Time%`
- `%Port%`
- `%Players%`
- `%Version%`
- `%Pastebin%`
- `%LastOnline%`
- `%FriendlyFire%`
- `%Whitelist%`
- `%Modded%`

`Infomation` keeps the old misspelled key for compatibility with the original config. Keep this spelling unless you also update the code.

## Add a Bot

1. Add another token to `.env`, for example:

```env
DISCORD_BOT_TOKEN_7=your_discord_bot_token_7
```

2. Copy `data/server.example.json` to `data/server_7.json`, then update `server_codename`, embed text, and message location.
3. Add one entry to `bots` in `setting.json`:

```json
{
  "key": "server_7",
  "name": "Server #7",
  "token_env": "DISCORD_BOT_TOKEN_7",
  "data_file": "server_7.json",
  "sync_guild_ids": [
    123456789012345678
  ],
  "enabled": true
}
```

4. Start the bot, then use `/here` in the target channel.
