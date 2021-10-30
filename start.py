#導入 模組
import requests
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import json, asyncio, datetime
intents = discord.Intents.all()

#讀取setting.json檔案
with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

#甚麼東西=甚麼
bot = commands.Bot(command_prefix='$', intents = intents)

#機器人上線
@bot.event
async def on_ready():
    counter = 0
    await bot.change_presence(activity=discord.Streaming(name="殘輝伺服器 已上線", url="https://www.twitch.tv/tw527e"))
    if counter == 0:
        print(f'《 Canhui 》機器人 上線了')
        counter = 1

#指令 - invite - 邀請連結
@bot.command()
async def invite(ctx):
    print(f'『{ctx.author}』 輸入 [伺服器邀請連結] 指令')
    await ctx.send("伺服器邀請連結:https://discord.gg/JQcM2WwYfH")

@bot.command()
@commands.is_owner()
async def here(ctx):
    print(f'『{ctx.author}』 輸入 [創建狀態顯示] 指令')
    await ctx.message.delete()
    message = await ctx.send("等等 等我一下")
    async def loop():
        while not bot.is_closed():
            now = str(datetime.datetime.now())
            loc = now.rfind('.')
            nnow = now[:loc]
            response = requests.get("https://api.scpslgame.com/serverinfo.php?players=true&&pastebin=true&version=true&online=true&ip=172.104.65.199&key=mg0IFGml9Mr8KnFkCSWUY2JM").json()
            if(response["Servers"][0]["Online"] == True):
                pastebin = response["Servers"][0]["Pastebin"]
                players = response["Servers"][0]["Players"]
                Ver = response["Servers"][0]["Version"]
                embed=discord.Embed(title="殘輝伺服器 《 Server #1 》 目前狀態", description="[For Beta Server]", color=0x28d252)
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/770662699239473162/f7f0cbe0c11eaa80645169ba69e11735.webp?size=128")
                embed.add_field(name="--------------------", value="伺服器狀態 - Server Status", inline=False)
                embed.add_field(name="伺服器狀態", value="已正常啟動", inline=True)
                embed.add_field(name="Server Status", value="Server started", inline=True)
                embed.add_field(name="--------------------", value="目前人數 - Players", inline=False)
                embed.add_field(name="目前人數", value=F"{players}", inline=True)
                embed.add_field(name="Players", value=F"{players}", inline=True)
                embed.add_field(name="--------------------", value="版本 - Version", inline=False)
                embed.add_field(name="版本", value=F"{Ver}", inline=True)
                embed.add_field(name="Version", value=F"{Ver}", inline=True)
                embed.add_field(name="--------------------", value="Pastebin", inline=False)
                embed.add_field(name="Pastebin 連結", value=F"[{pastebin}](https://pastebin.com/{pastebin})", inline=True)
                embed.add_field(name="Pastebin", value=F"[{pastebin}](https://pastebin.com/{pastebin})", inline=True)
                embed.set_footer(text=F"此資料上次更新時間 {nnow} • Last updated {nnow} (GMT+8)", icon_url=ctx.author.avatar_url)
            else:
                pastebin = response["Servers"][0]["Pastebin"]
                Ver = response["Servers"][0]["Version"]
                embed=discord.Embed(title="殘輝伺服器 《 Server #1 》 目前狀態", description="[For Beta Server]", color=0xff0000)
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/770662699239473162/f7f0cbe0c11eaa80645169ba69e11735.webp?size=128")
                embed.add_field(name="--------------------", value="伺服器狀態 - Server Status", inline=False)
                embed.add_field(name="伺服器狀態", value="關服了 不然就是炸了", inline=True)
                embed.add_field(name="Server Status", value="Server closed", inline=True)
                embed.add_field(name="--------------------", value="目前人數 - Players", inline=False)
                embed.add_field(name="目前人數", value="沒有", inline=True)
                embed.add_field(name="Players", value="Nope", inline=True)
                embed.add_field(name="--------------------", value="版本 - Version", inline=False)
                embed.add_field(name="版本", value=F"{Ver}", inline=True)
                embed.add_field(name="Version", value=F"{Ver}", inline=True)
                embed.add_field(name="--------------------", value="Pastebin", inline=False)
                embed.add_field(name="Pastebin 連結", value=F"[{pastebin}](https://pastebin.com/{pastebin})", inline=True)
                embed.add_field(name="Pastebin", value=F"[{pastebin}](https://pastebin.com/{pastebin})", inline=True)
                embed.add_field
                embed.set_footer(text=F"此資料上次更新時間 {nnow} • Last updated {nnow} (GMT+8)", icon_url=ctx.author.avatar_url)
            await message.edit(embed=embed, content="")
            print(F"[{nnow}] 伺服器資料已更新")
            await asyncio.sleep(15)
    bot.loop.create_task(loop())

if __name__ == "__main__":
    #Token-金鑰(setting.json)
    bot.run(jdata['Token'])