#導入 模組
import requests
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import json, asyncio
from datetime import datetime,timezone,timedelta
intents = discord.Intents.all()

#讀取setting.json檔案
with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot1 = commands.Bot(command_prefix='\|/1', intents = intents)

@bot1.event
async def on_ready():
    counter = 0
    await bot1.change_presence(activity=discord.Streaming(name="\|/準備中\|/", url="https://www.twitch.tv/tw527e"))
    if counter == 0:
        print(f'《 {bot1.user} 》上線了')
        counter = 1
    if(jdata['Server 2'][0]['Switch']):
        await bot2.start(jdata['Server 2'][0]['Discord Bot Token'])

@bot1.command()
@commands.is_owner()
async def here(ctx):
    print(f'[Server #1]『{ctx.author}』 輸入 [創建狀態顯示] 指令')
    await ctx.message.delete()
    message = await ctx.send("等等 等我一下")
    jdata['Server 1'][0]['Status Guild'] = message.guild.id
    jdata['Server 1'][0]['Status Channel'] = message.channel.id
    jdata['Server 1'][0]['Status Message'] = message.id
    with open('setting.json', 'w', encoding='utf8') as f:
            json.dump(jdata, f, indent=4)

if(jdata['Server 2'][0]['Switch']):
    bot2 = commands.Bot(command_prefix='\|/2', intents = intents)

    @bot2.event
    async def on_ready():
        counter = 0
        await bot2.change_presence(activity=discord.Streaming(name="\|/準備中\|/", url="https://www.twitch.tv/tw527e"))
        if counter == 0:
            print(f'《 {bot2.user} 》上線了')
            counter = 1
        if(jdata['Server 3'][0]['Switch']):
            await bot3.start(jdata['Server 3'][0]['Discord Bot Token'])

    @bot2.command()
    @commands.is_owner()
    async def here(ctx):
        print(f'[Server #2]『{ctx.author}』 輸入 [創建狀態顯示] 指令')
        await ctx.message.delete()
        message = await ctx.send("等等 等我一下")
        jdata['Server 2'][0]['Status Guild'] = message.guild.id
        jdata['Server 2'][0]['Status Channel'] = message.channel.id
        jdata['Server 2'][0]['Status Message'] = message.id
        with open('setting.json', 'w', encoding='utf8') as f:
                json.dump(jdata, f, indent=4)

if(jdata['Server 3'][0]['Switch']):
    bot3 = commands.Bot(command_prefix='\|/3', intents = intents)

    @bot3.event
    async def on_ready():
        counter = 0
        await bot3.change_presence(activity=discord.Streaming(name="\|/準備中\|/", url="https://www.twitch.tv/tw527e"))
        if counter == 0:
            print(f'《 {bot3.user} 》上線了')
            counter = 1
        bot1.loop.create_task(Server_Status())

    @bot3.command()
    @commands.is_owner()
    async def here(ctx):
        print(f'[Server #3]『{ctx.author}』 輸入 [創建狀態顯示] 指令')
        await ctx.message.delete()
        message = await ctx.send("等等 等我一下")
        jdata['Server 3'][0]['Status Guild'] = message.guild.id
        jdata['Server 3'][0]['Status Channel'] = message.channel.id
        jdata['Server 3'][0]['Status Message'] = message.id
        with open('setting.json', 'w', encoding='utf8') as f:
                json.dump(jdata, f, indent=4)

async def Server_Status():
    while not bot1.is_closed():
        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
        dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
        owner = bot1.get_user(356361726427660288)
        response = requests.get(f"https://api.scpslgame.com/serverinfo.php?key={jdata['API Token']}&id={jdata['Account ID']}&lo=true&players=true&list=true&info=true&pastebin=true&version=true&flags=true&nicknames=true&online=true").json()
        jdata['Do not change this'] = response
        with open('setting.json', 'w', encoding='utf8') as f:
            json.dump(jdata, f, indent=4)
        
        Server_Number = 1
        channel = bot1.get_guild(jdata[f'Server {Server_Number}'][0]['Status Guild']).get_channel(jdata[f'Server {Server_Number}'][0]['Status Channel'])
        message = await channel.fetch_message(jdata[f'Server {Server_Number}'][0]['Status Message'])

        if(jdata['Do not change this']["Success"]):
            if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Online"]):
                Players = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Players"]
                Port = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Port"]
                Ver = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Version"]
                Pastebin = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Pastebin"]
                LastOnline = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["LastOnline"]

                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["FF"]):
                    FFChinese = ":o: 同隊傷害"
                    FFEnglish = ":o: Friendly Fire"
                else:
                    FFChinese = ":x: 同隊傷害"
                    FFEnglish = ":x: Friendly Fire"
                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["WL"]):
                    WLChinese = ":o: 白名單"
                    WLEnglish = ":o: WhiteList"
                else:
                    WLChinese = ":x: 白名單"
                    WLEnglish = ":x: WhiteList"
                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Modded"]):
                    ModdedChinese = ":o: 插件"
                    ModdedEnglish = ":o: Modded"
                else:
                    ModdedChinese = ":x: 插件"
                    ModdedEnglish = ":x: Modded"

                await bot1.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"{Players}", type=discord.ActivityType.watching))
                embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0x28d252)
                embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
                embed.add_field(name="狀態", value="已正常啟動", inline=True)
                embed.add_field(name="Status", value="Server started", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
                embed.add_field(name="伺服器連接埠", value=f"{Port}", inline=True)
                embed.add_field(name="Server Port", value=f"{Port}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
                embed.add_field(name="目前人數", value=F"{Players}", inline=True)
                embed.add_field(name="Players", value=F"{Players}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
                embed.add_field(name="版本", value=F"{Ver}", inline=True)
                embed.add_field(name="Version", value=F"{Ver}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
                embed.add_field(name="Pastebin 連結", value=F"[{Pastebin}](https://pastebin.com/{Pastebin})", inline=True)
                embed.add_field(name="Pastebin Link", value=F"[{Pastebin}](https://pastebin.com/{Pastebin})", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
                embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
                embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
                embed.add_field(name="最後上線日期", value=F"{LastOnline}", inline=True)
                embed.add_field(name="Last Online Date", value=F"{LastOnline}", inline=True)
                embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
            else:
                Port = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Port"]
                LastOnline = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["LastOnline"]

                FFChinese = ":warning: 同隊傷害 "
                FFEnglish = ":warning: Friendly Fire"

                WLChinese = ":warning: 白名單"
                WLEnglish = ":warning: WhiteList"
                    
                ModdedChinese = ":warning: 插件"
                ModdedEnglish = ":warning: Modded"

                await bot1.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f"\|/伺服器已關閉\|/", type=discord.ActivityType.watching))
                embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0xFF0000)
                embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
                embed.add_field(name="狀態", value="伺服器已關閉", inline=True)
                embed.add_field(name="Status", value="Server is down", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
                embed.add_field(name="伺服器連接埠", value=f"{Port}", inline=True)
                embed.add_field(name="Server Port", value=f"{Port}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
                embed.add_field(name="目前人數", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Players", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
                embed.add_field(name="版本", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Version", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
                embed.add_field(name="Pastebin 連結", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Pastebin Link", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
                embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
                embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
                embed.add_field(name="最後上線日期", value=F"{LastOnline}", inline=True)
                embed.add_field(name="Last Online Date", value=F"{LastOnline}", inline=True)
                embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
        else:
            FFChinese = ":warning: 同隊傷害 "
            FFEnglish = ":warning: Friendly Fire"

            WLChinese = ":warning: 白名單"
            WLEnglish = ":warning: WhiteList"
                
            ModdedChinese = ":warning: 插件"
            ModdedEnglish = ":warning: Modded"

            await bot1.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f"\|/無法取得狀態\|/", type=discord.ActivityType.watching))
            embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0xFF0000)
            embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
            embed.add_field(name="狀態", value="無法取得狀態", inline=True)
            embed.add_field(name="Status", value="The status cannot be obtained", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
            embed.add_field(name="伺服器連接埠", value=f"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Server Port", value=f"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
            embed.add_field(name="目前人數", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Players", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
            embed.add_field(name="版本", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Version", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
            embed.add_field(name="Pastebin 連結", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Pastebin Link", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
            embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
            embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
            embed.add_field(name="最後上線日期", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Last Online Date", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
        await message.edit(embed=embed, content="")
        print(F"[Server #{Server_Number}][{dt2.strftime('%Y-%m-%d %H:%M:%S')}] 伺服器資料已更新")
    
        Server_Number = 2
        channel = bot2.get_guild(jdata[f'Server {Server_Number}'][0]['Status Guild']).get_channel(jdata[f'Server {Server_Number}'][0]['Status Channel'])
        message = await channel.fetch_message(jdata[f'Server {Server_Number}'][0]['Status Message'])

        if(jdata['Do not change this']["Success"]):
            if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Online"]):
                Players = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Players"]
                Port = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Port"]
                Ver = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Version"]
                Pastebin = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Pastebin"]
                LastOnline = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["LastOnline"]

                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["FF"]):
                    FFChinese = ":o: 同隊傷害"
                    FFEnglish = ":o: Friendly Fire"
                else:
                    FFChinese = ":x: 同隊傷害"
                    FFEnglish = ":x: Friendly Fire"
                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["WL"]):
                    WLChinese = ":o: 白名單"
                    WLEnglish = ":o: WhiteList"
                else:
                    WLChinese = ":x: 白名單"
                    WLEnglish = ":x: WhiteList"
                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Modded"]):
                    ModdedChinese = ":o: 插件"
                    ModdedEnglish = ":o: Modded"
                else:
                    ModdedChinese = ":x: 插件"
                    ModdedEnglish = ":x: Modded"

                await bot2.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"{Players}", type=discord.ActivityType.watching))
                embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0x28d252)
                embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
                embed.add_field(name="狀態", value="已正常啟動", inline=True)
                embed.add_field(name="Status", value="Server started", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
                embed.add_field(name="伺服器連接埠", value=f"{Port}", inline=True)
                embed.add_field(name="Server Port", value=f"{Port}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
                embed.add_field(name="目前人數", value=F"{Players}", inline=True)
                embed.add_field(name="Players", value=F"{Players}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
                embed.add_field(name="版本", value=F"{Ver}", inline=True)
                embed.add_field(name="Version", value=F"{Ver}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
                embed.add_field(name="Pastebin 連結", value=F"[{Pastebin}](https://pastebin.com/{Pastebin})", inline=True)
                embed.add_field(name="Pastebin Link", value=F"[{Pastebin}](https://pastebin.com/{Pastebin})", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
                embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
                embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
                embed.add_field(name="最後上線日期", value=F"{LastOnline}", inline=True)
                embed.add_field(name="Last Online Date", value=F"{LastOnline}", inline=True)
                embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
            else:
                Port = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Port"]
                LastOnline = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["LastOnline"]

                FFChinese = ":warning: 同隊傷害 "
                FFEnglish = ":warning: Friendly Fire"

                WLChinese = ":warning: 白名單"
                WLEnglish = ":warning: WhiteList"
                    
                ModdedChinese = ":warning: 插件"
                ModdedEnglish = ":warning: Modded"

                await bot2.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f"\|/伺服器已關閉\|/", type=discord.ActivityType.watching))
                embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0xFF0000)
                embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
                embed.add_field(name="狀態", value="伺服器已關閉", inline=True)
                embed.add_field(name="Status", value="Server is down", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
                embed.add_field(name="伺服器連接埠", value=f"{Port}", inline=True)
                embed.add_field(name="Server Port", value=f"{Port}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
                embed.add_field(name="目前人數", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Players", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
                embed.add_field(name="版本", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Version", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
                embed.add_field(name="Pastebin 連結", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Pastebin Link", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
                embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
                embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
                embed.add_field(name="最後上線日期", value=F"{LastOnline}", inline=True)
                embed.add_field(name="Last Online Date", value=F"{LastOnline}", inline=True)
                embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
        else:
            FFChinese = ":warning: 同隊傷害 "
            FFEnglish = ":warning: Friendly Fire"

            WLChinese = ":warning: 白名單"
            WLEnglish = ":warning: WhiteList"
                
            ModdedChinese = ":warning: 插件"
            ModdedEnglish = ":warning: Modded"

            await bot2.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f"\|/無法取得狀態\|/", type=discord.ActivityType.watching))
            embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0xFF0000)
            embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
            embed.add_field(name="狀態", value="無法取得狀態", inline=True)
            embed.add_field(name="Status", value="The status cannot be obtained", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
            embed.add_field(name="伺服器連接埠", value=f"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Server Port", value=f"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
            embed.add_field(name="目前人數", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Players", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
            embed.add_field(name="版本", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Version", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
            embed.add_field(name="Pastebin 連結", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Pastebin Link", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
            embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
            embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
            embed.add_field(name="最後上線日期", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Last Online Date", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
        await message.edit(embed=embed, content="")
        print(F"[Server #{Server_Number}][{dt2.strftime('%Y-%m-%d %H:%M:%S')}] 伺服器資料已更新")

        Server_Number = 3
        channel = bot3.get_guild(jdata[f'Server {Server_Number}'][0]['Status Guild']).get_channel(jdata[f'Server {Server_Number}'][0]['Status Channel'])
        message = await channel.fetch_message(jdata[f'Server {Server_Number}'][0]['Status Message'])

        if(jdata['Do not change this']["Success"]):
            if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Online"]):
                Players = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Players"]
                Port = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Port"]
                Ver = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Version"]
                Pastebin = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Pastebin"]
                LastOnline = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["LastOnline"]

                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["FF"]):
                    FFChinese = ":o: 同隊傷害"
                    FFEnglish = ":o: Friendly Fire"
                else:
                    FFChinese = ":x: 同隊傷害"
                    FFEnglish = ":x: Friendly Fire"
                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["WL"]):
                    WLChinese = ":o: 白名單"
                    WLEnglish = ":o: WhiteList"
                else:
                    WLChinese = ":x: 白名單"
                    WLEnglish = ":x: WhiteList"
                if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Modded"]):
                    ModdedChinese = ":o: 插件"
                    ModdedEnglish = ":o: Modded"
                else:
                    ModdedChinese = ":x: 插件"
                    ModdedEnglish = ":x: Modded"

                await bot3.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"{Players}", type=discord.ActivityType.watching))
                embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0x28d252)
                embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
                embed.add_field(name="狀態", value="已正常啟動", inline=True)
                embed.add_field(name="Status", value="Server started", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
                embed.add_field(name="伺服器連接埠", value=f"{Port}", inline=True)
                embed.add_field(name="Server Port", value=f"{Port}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
                embed.add_field(name="目前人數", value=F"{Players}", inline=True)
                embed.add_field(name="Players", value=F"{Players}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
                embed.add_field(name="版本", value=F"{Ver}", inline=True)
                embed.add_field(name="Version", value=F"{Ver}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
                embed.add_field(name="Pastebin 連結", value=F"[{Pastebin}](https://pastebin.com/{Pastebin})", inline=True)
                embed.add_field(name="Pastebin Link", value=F"[{Pastebin}](https://pastebin.com/{Pastebin})", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
                embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
                embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
                embed.add_field(name="最後上線日期", value=F"{LastOnline}", inline=True)
                embed.add_field(name="Last Online Date", value=F"{LastOnline}", inline=True)
                embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
            else:
                Port = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Port"]
                LastOnline = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["LastOnline"]

                FFChinese = ":warning: 同隊傷害 "
                FFEnglish = ":warning: Friendly Fire"

                WLChinese = ":warning: 白名單"
                WLEnglish = ":warning: WhiteList"
                    
                ModdedChinese = ":warning: 插件"
                ModdedEnglish = ":warning: Modded"

                await bot3.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f"\|/伺服器已關閉\|/", type=discord.ActivityType.watching))
                embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0xFF0000)
                embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
                embed.add_field(name="狀態", value="伺服器已關閉", inline=True)
                embed.add_field(name="Status", value="Server is down", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
                embed.add_field(name="伺服器連接埠", value=f"{Port}", inline=True)
                embed.add_field(name="Server Port", value=f"{Port}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
                embed.add_field(name="目前人數", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Players", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
                embed.add_field(name="版本", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Version", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
                embed.add_field(name="Pastebin 連結", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="Pastebin Link", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
                embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
                embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
                embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
                embed.add_field(name="最後上線日期", value=F"{LastOnline}", inline=True)
                embed.add_field(name="Last Online Date", value=F"{LastOnline}", inline=True)
                embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
        else:
            FFChinese = ":warning: 同隊傷害 "
            FFEnglish = ":warning: Friendly Fire"

            WLChinese = ":warning: 白名單"
            WLEnglish = ":warning: WhiteList"
                
            ModdedChinese = ":warning: 插件"
            ModdedEnglish = ":warning: Modded"

            await bot3.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f"\|/無法取得狀態\|/", type=discord.ActivityType.watching))
            embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][0]['Status Title']}", description=f"{jdata[f'Server {Server_Number}'][0]['Server Description']}", color=0xFF0000)
            embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][0]['Server Icon']}")
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="狀態－Status", inline=False)
            embed.add_field(name="狀態", value="無法取得狀態", inline=True)
            embed.add_field(name="Status", value="The status cannot be obtained", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="伺服器連接埠－Server Port", inline=False)
            embed.add_field(name="伺服器連接埠", value=f"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Server Port", value=f"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="目前人數－Players", inline=False)
            embed.add_field(name="目前人數", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Players", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="版本－Version", inline=False)
            embed.add_field(name="版本", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Version", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="Pastebin", inline=False)
            embed.add_field(name="Pastebin 連結", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Pastebin Link", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="詳細狀態－Infomation", inline=False)
            embed.add_field(name="詳細資訊", value=F"{FFChinese}｜{WLChinese}｜{ModdedChinese}", inline=True)
            embed.add_field(name="Infomation", value=F"{FFEnglish}｜{WLEnglish}｜{ModdedEnglish}", inline=True)
            embed.add_field(name="＝＝＝＝＝＝＝＝＝＝＝", value="最後上線日期－Last Online Date", inline=False)
            embed.add_field(name="最後上線日期", value=F"[未知](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.add_field(name="Last Online Date", value=F"[Unknown](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=True)
            embed.set_footer(text=F"此資料上次更新時間 {dt2.strftime('%Y-%m-%d %H:%M:%S')} • Last updated {dt2.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8) 此程式由 誠誠#7773 製作", icon_url=owner.avatar_url)
        await message.edit(embed=embed, content="")
        print(F"[Server #{Server_Number}][{dt2.strftime('%Y-%m-%d %H:%M:%S')}] 伺服器資料已更新")
        if(jdata['Do not change this']["Success"]):
            await asyncio.sleep(jdata['Do not change this']["Cooldown"])
        else:
            await asyncio.sleep(24)
        
bot1.run(jdata['Server 1'][0]['Discord Bot Token'])