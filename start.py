#導入 模組
import discord
import requests
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import json, asyncio
from datetime import datetime,timezone,timedelta
intents = discord.Intents.all()

#讀取setting.json檔案
with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot1 = commands.Bot(command_prefix='\\|/', intents = intents)

@bot1.event
async def on_ready():
    counter = 0
    await bot1.change_presence(activity=discord.Streaming(name="\|/準備中\|/", url="https://www.twitch.tv/tw527e"))
    if counter == 0:
        print(f'《 {bot1.user} 》上線了')
        counter = 1
    await bot2.start(jdata['Server 2'][0]['Discord Bot Token'])

@bot1.command()
@commands.is_owner()
async def here(ctx):
    print(f'[Server #1]『{ctx.author}』 輸入 [創建狀態顯示] 指令')
    await ctx.message.delete()
    message = await ctx.send("等等 等我一下")
    jdata['Server 1'][0]['Message Guild ID'] = message.guild.id
    jdata['Server 1'][0]['Message Channel ID'] = message.channel.id
    jdata['Server 1'][0]['Message ID'] = message.id
    with open('setting.json', 'w', encoding='utf8') as f:
            json.dump(jdata, f, indent=4)

bot2 = commands.Bot(command_prefix='\|/2', intents = intents)

@bot2.event
async def on_ready():
    counter = 0
    await bot2.change_presence(activity=discord.Streaming(name="\|/準備中\|/", url="https://www.twitch.tv/tw527e"))
    if counter == 0:
        print(f'《 {bot2.user} 》上線了')
        counter = 1
    await bot3.start(jdata['Server 3'][0]['Discord Bot Token'])

@bot2.command()
@commands.is_owner()
async def here(ctx):
    print(f'[Server #2]『{ctx.author}』 輸入 [創建狀態顯示] 指令')
    await ctx.message.delete()
    message = await ctx.send("等等 等我一下")
    jdata['Server 2'][0]['Message Guild ID'] = message.guild.id
    jdata['Server 2'][0]['Message Channel ID'] = message.channel.id
    jdata['Server 2'][0]['Message ID'] = message.id
    with open('setting.json', 'w', encoding='utf8') as f:
            json.dump(jdata, f, indent=4)

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
    jdata['Server 3'][0]['Message Guild ID'] = message.guild.id
    jdata['Server 3'][0]['Message Channel ID'] = message.channel.id
    jdata['Server 3'][0]['Message ID'] = message.id
    with open('setting.json', 'w', encoding='utf8') as f:
            json.dump(jdata, f, indent=4)

async def Server_Status():
    while not bot1.is_closed():
        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
        dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
        owner = bot1.get_user(356361726427660288)
        response = requests.get(f"https://api.scpslgame.com/serverinfo.php?key={jdata['API Token']}&id={jdata['Account ID']}&lo=true&players=true&list=true&info=true&pastebin=true&version=true&flags=true&nicknames=true&online=true").json()
        jdata['Do not change this'] = response
        jdata["Last Update Time"] = dt2.strftime('%Y-%m-%d %H:%M:%S')
        with open('setting.json', 'w', encoding='utf8') as f:
            json.dump(jdata, f, indent=4)
        
        Server_Number = 1
        
        while not Server_Number == 4:
            if(Server_Number == 1):
                channel = bot1.get_guild(jdata[f'Server {Server_Number}'][0]['Message Guild ID']).get_channel(jdata[f'Server {Server_Number}'][0]['Message Channel ID'])
            if(Server_Number == 2):
                channel = bot2.get_guild(jdata[f'Server {Server_Number}'][0]['Message Guild ID']).get_channel(jdata[f'Server {Server_Number}'][0]['Message Channel ID'])
            if(Server_Number == 3):
                channel = bot3.get_guild(jdata[f'Server {Server_Number}'][0]['Message Guild ID']).get_channel(jdata[f'Server {Server_Number}'][0]['Message Channel ID'])
            message = await channel.fetch_message(jdata[f'Server {Server_Number}'][0]['Message ID'])
            if(jdata['Do not change this']["Success"]):
                if(len(jdata['Do not change this']["Servers"]) >= Server_Number):
                    if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Online"]):
                        Players = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Players"]
                        Port = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Port"]
                        Ver = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Version"]
                        Pastebin = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Pastebin"]
                        LastOnline = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["LastOnline"]

                        if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["FF"]):
                            FF1 = jdata[f'Server {Server_Number}'][1]['Friendly Fire On'][0]
                            FF2 = jdata[f'Server {Server_Number}'][1]['Friendly Fire On'][1]
                        else:
                            FF1 = jdata[f'Server {Server_Number}'][1]['Friendly Fire Off'][0]
                            FF2 = jdata[f'Server {Server_Number}'][1]['Friendly Fire Off'][1]

                        if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["WL"]):
                            WL1 = jdata[f'Server {Server_Number}'][1]['Whitelist On'][0]
                            WL2 = jdata[f'Server {Server_Number}'][1]['Whitelist On'][1]
                        else:
                            WL1 = jdata[f'Server {Server_Number}'][1]['Whitelist Off'][0]
                            WL2 = jdata[f'Server {Server_Number}'][1]['Whitelist Off'][1]

                        if(jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Modded"]):
                            Modded1 = jdata[f'Server {Server_Number}'][1]['Modded On'][0]
                            Modded2 = jdata[f'Server {Server_Number}'][1]['Modded On'][1]
                        else:
                            Modded1 = jdata[f'Server {Server_Number}'][1]['Modded Off'][0]
                            Modded2 = jdata[f'Server {Server_Number}'][1]['Modded Off'][1]

                        if(Server_Number == 1):
                            await bot1.change_presence(status=discord.Status.online, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Started'].replace("%Players%", Players), type=discord.ActivityType.watching))
                        if(Server_Number == 2):
                            await bot2.change_presence(status=discord.Status.online, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Started'].replace("%Players%", Players), type=discord.ActivityType.watching))
                        if(Server_Number == 3):
                            await bot3.change_presence(status=discord.Status.online, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Started'].replace("%Players%", Players), type=discord.ActivityType.watching))
                        #Embed
                        embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][1]['Message Title']}", description=f"{jdata[f'Server {Server_Number}'][1]['Server Description']}", color=0x28d252)
                        embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][1]['Server Icon']}")
                        #狀態 - Status
                        if(jdata[f'Server {Server_Number}'][1]['Status'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Status'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Status'][2], value=jdata[f'Server {Server_Number}'][1]['Status Started'][0], inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Status'][3], value=jdata[f'Server {Server_Number}'][1]['Status Started'][1], inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Port'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Port'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Port'][2], value=jdata[f'Server {Server_Number}'][1]['Port Started'][0].replace("%Port%", f"{Port}"), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Port'][3], value=jdata[f'Server {Server_Number}'][1]['Port Started'][1].replace("%Port%", f"{Port}"), inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Players'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Players'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Players'][2], value=jdata[f'Server {Server_Number}'][1]['Players Started'][0].replace("%Players%", Players), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Players'][3], value=jdata[f'Server {Server_Number}'][1]['Players Started'][1].replace("%Players%", Players), inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Version'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Version'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Version'][2], value=jdata[f'Server {Server_Number}'][1]['Version Started'][0].replace("%Version%", Ver), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Version'][3], value=jdata[f'Server {Server_Number}'][1]['Version Started'][1].replace("%Version%", Ver), inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Pastebin'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Pastebin'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Pastebin'][2], value=jdata[f'Server {Server_Number}'][1]['Pastebin Started'][0].replace("%Pastebin%", Pastebin), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Pastebin'][3], value=jdata[f'Server {Server_Number}'][1]['Pastebin Started'][1].replace("%Pastebin%", Pastebin), inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Infomation'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Infomation'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Infomation'][2], value=jdata[f'Server {Server_Number}'][1]['Infomation Started'][0].replace("%FriendlyFire%", FF1).replace("%Whitelist%", WL1).replace("%Modded%", Modded1), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Infomation'][3], value=jdata[f'Server {Server_Number}'][1]['Infomation Started'][1].replace("%FriendlyFire%", FF2).replace("%Whitelist%", WL2).replace("%Modded%", Modded2), inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['LastOnline'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['LastOnline'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['LastOnline'][2], value=jdata[f'Server {Server_Number}'][1]['LastOnline Started'][0].replace("%LastOnline%", LastOnline), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['LastOnline'][3], value=jdata[f'Server {Server_Number}'][1]['LastOnline Started'][1].replace("%LastOnline%", LastOnline), inline=True)
                        embed.set_footer(text=jdata[f'Server {Server_Number}'][1]['Last Updated'].replace("%Time%", dt2.strftime('%Y-%m-%d %H:%M:%S')) + "Made by 誠誠#7773", icon_url=owner.avatar_url)
                    else:
                        Port = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["Port"]
                        LastOnline = jdata['Do not change this']["Servers"][jdata[f'Server {Server_Number}'][0]['Server Codename']]["LastOnline"]

                        FF1 = jdata[f'Server {Server_Number}'][1]['Friendly Fire Warning'][0]
                        FF2 = jdata[f'Server {Server_Number}'][1]['Friendly Fire Warning'][1]

                        WL1 = jdata[f'Server {Server_Number}'][1]['Whitelist Warning'][0]
                        WL2 = jdata[f'Server {Server_Number}'][1]['Whitelist Warning'][1]
                            
                        Modded1 = jdata[f'Server {Server_Number}'][1]['Modded Warning'][0]
                        Modded2 = jdata[f'Server {Server_Number}'][1]['Modded Warning'][1]

                        if(Server_Number == 1):
                            await bot1.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Closed'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                        if(Server_Number == 2):
                            await bot2.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Closed'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                        if(Server_Number == 3):
                            await bot3.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Closed'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                        #Embed
                        embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][1]['Message Title']}", description=f"{jdata[f'Server {Server_Number}'][1]['Server Description']}", color=0xFF0000)
                        embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][1]['Server Icon']}")
                        #狀態 - Status
                        if(jdata[f'Server {Server_Number}'][1]['Status'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Status'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Status'][2], value=jdata[f'Server {Server_Number}'][1]['Status Closed'][0], inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Status'][3], value=jdata[f'Server {Server_Number}'][1]['Status Closed'][1], inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Port'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Port'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Port'][2], value=jdata[f'Server {Server_Number}'][1]['Port Closed'][0].replace("%Port%", f"{Port}"), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Port'][3], value=jdata[f'Server {Server_Number}'][1]['Port Closed'][1].replace("%Port%", f"{Port}"), inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Players'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Players'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Players'][2], value=jdata[f'Server {Server_Number}'][1]['Players Closed'][0], inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Players'][3], value=jdata[f'Server {Server_Number}'][1]['Players Closed'][1], inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Version'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Version'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Version'][2], value=jdata[f'Server {Server_Number}'][1]['Version Closed'][0], inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Version'][3], value=jdata[f'Server {Server_Number}'][1]['Version Closed'][1], inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Pastebin'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Pastebin'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Pastebin'][2], value=jdata[f'Server {Server_Number}'][1]['Pastebin Closed'][0], inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Pastebin'][3], value=jdata[f'Server {Server_Number}'][1]['Pastebin Closed'][1], inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['Infomation'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Infomation'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Infomation'][2], value=jdata[f'Server {Server_Number}'][1]['Infomation Closed'][0].replace("%FriendlyFire%", FF1).replace("%Whitelist%", WL1).replace("%Modded%", Modded1), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Infomation'][3], value=jdata[f'Server {Server_Number}'][1]['Infomation Closed'][1].replace("%FriendlyFire%", FF2).replace("%Whitelist%", WL2).replace("%Modded%", Modded2), inline=True)
                        if(jdata[f'Server {Server_Number}'][1]['LastOnline'][0]):
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['LastOnline'][1], inline=False)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['LastOnline'][2], value=jdata[f'Server {Server_Number}'][1]['LastOnline Closed'][0].replace("%LastOnline%", LastOnline), inline=True)
                            embed.add_field(name=jdata[f'Server {Server_Number}'][1]['LastOnline'][3], value=jdata[f'Server {Server_Number}'][1]['LastOnline Closed'][1].replace("%LastOnline%", LastOnline), inline=True)
                        embed.set_footer(text=jdata[f'Server {Server_Number}'][1]['Last Updated'].replace("%Time%", dt2.strftime('%Y-%m-%d %H:%M:%S')) + "Made by 誠誠#7773", icon_url=owner.avatar_url)
                else:
                    FF1 = jdata[f'Server {Server_Number}'][1]['Friendly Fire Warning'][0]
                    FF2 = jdata[f'Server {Server_Number}'][1]['Friendly Fire Warning'][1]

                    WL1 = jdata[f'Server {Server_Number}'][1]['Whitelist Warning'][0]
                    WL2 = jdata[f'Server {Server_Number}'][1]['Whitelist Warning'][1]
                            
                    Modded1 = jdata[f'Server {Server_Number}'][1]['Modded Warning'][0]
                    Modded2 = jdata[f'Server {Server_Number}'][1]['Modded Warning'][1]

                    if(Server_Number == 1):
                        await bot1.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Warning'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                    if(Server_Number == 2):
                        await bot2.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Warning'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                    if(Server_Number == 3):
                        await bot3.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Warning'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                    #Embed
                    embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][1]['Message Title']}", description=f"{jdata[f'Server {Server_Number}'][1]['Server Description']}", color=0xFF0000)
                    embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][1]['Server Icon']}")
                    #狀態 - Status
                    if(jdata[f'Server {Server_Number}'][1]['Status'][0]):
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Status'][1], inline=False)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Status'][2], value=jdata[f'Server {Server_Number}'][1]['Status Warning'][0], inline=True)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Status'][3], value=jdata[f'Server {Server_Number}'][1]['Status Warning'][1], inline=True)
                    if(jdata[f'Server {Server_Number}'][1]['Port'][0]):
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Port'][1], inline=False)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Port'][2], value=jdata[f'Server {Server_Number}'][1]['Port Warning'][0], inline=True)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Port'][3], value=jdata[f'Server {Server_Number}'][1]['Port Warning'][1], inline=True)
                    if(jdata[f'Server {Server_Number}'][1]['Players'][0]):
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Players'][1], inline=False)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Players'][2], value=jdata[f'Server {Server_Number}'][1]['Players Warning'][0], inline=True)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Players'][3], value=jdata[f'Server {Server_Number}'][1]['Players Warning'][1], inline=True)
                    if(jdata[f'Server {Server_Number}'][1]['Version'][0]):
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Version'][1], inline=False)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Version'][2], value=jdata[f'Server {Server_Number}'][1]['Version Warning'][0], inline=True)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Version'][3], value=jdata[f'Server {Server_Number}'][1]['Version Warning'][1], inline=True)
                    if(jdata[f'Server {Server_Number}'][1]['Pastebin'][0]):
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Pastebin'][1], inline=False)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Pastebin'][2], value=jdata[f'Server {Server_Number}'][1]['Pastebin Warning'][0], inline=True)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Pastebin'][3], value=jdata[f'Server {Server_Number}'][1]['Pastebin Warning'][1], inline=True)
                    if(jdata[f'Server {Server_Number}'][1]['Infomation'][0]):
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Infomation'][1], inline=False)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Infomation'][2], value=jdata[f'Server {Server_Number}'][1]['Infomation Warning'][0].replace("%FriendlyFire%", FF1).replace("%Whitelist%", WL1).replace("%Modded%", Modded1), inline=True)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Infomation'][3], value=jdata[f'Server {Server_Number}'][1]['Infomation Warning'][1].replace("%FriendlyFire%", FF2).replace("%Whitelist%", WL2).replace("%Modded%", Modded2), inline=True)
                    if(jdata[f'Server {Server_Number}'][1]['LastOnline'][0]):
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['LastOnline'][1], inline=False)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['LastOnline'][2], value=jdata[f'Server {Server_Number}'][1]['LastOnline Warning'][0], inline=True)
                        embed.add_field(name=jdata[f'Server {Server_Number}'][1]['LastOnline'][3], value=jdata[f'Server {Server_Number}'][1]['LastOnline Warning'][1], inline=True)
                    embed.set_footer(text=jdata[f'Server {Server_Number}'][1]['Last Updated'].replace("%Time%", dt2.strftime('%Y-%m-%d %H:%M:%S')) + "Made by 誠誠#7773", icon_url=owner.avatar_url)
            else:
                FF1 = jdata[f'Server {Server_Number}'][1]['Friendly Fire Warning'][0]
                FF2 = jdata[f'Server {Server_Number}'][1]['Friendly Fire Warning'][1]

                WL1 = jdata[f'Server {Server_Number}'][1]['Whitelist Warning'][0]
                WL2 = jdata[f'Server {Server_Number}'][1]['Whitelist Warning'][1]
                        
                Modded1 = jdata[f'Server {Server_Number}'][1]['Modded Warning'][0]
                Modded2 = jdata[f'Server {Server_Number}'][1]['Modded Warning'][1]
                
                if(Server_Number == 1):
                    await bot1.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Warning'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                if(Server_Number == 2):
                    await bot2.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Warning'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                if(Server_Number == 3):
                    await bot3.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=jdata[f'Server {Server_Number}'][2]['Bot Status Warning'].replace("＼｜／", "\|/"), type=discord.ActivityType.watching))
                #Embed
                embed=discord.Embed(title=f"{jdata[f'Server {Server_Number}'][1]['Message Title']}", description=f"{jdata[f'Server {Server_Number}'][1]['Server Description']}", color=0xFF0000)
                embed.set_thumbnail(url=f"{jdata[f'Server {Server_Number}'][1]['Server Icon']}")
                #狀態 - Status
                if(jdata[f'Server {Server_Number}'][1]['Status'][0]):
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Status'][1], inline=False)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Status'][2], value=jdata[f'Server {Server_Number}'][1]['Status Warning'][0], inline=True)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Status'][3], value=jdata[f'Server {Server_Number}'][1]['Status Warning'][1], inline=True)
                if(jdata[f'Server {Server_Number}'][1]['Port'][0]):
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Port'][1], inline=False)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Port'][2], value=jdata[f'Server {Server_Number}'][1]['Port Warning'][0], inline=True)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Port'][3], value=jdata[f'Server {Server_Number}'][1]['Port Warning'][1], inline=True)
                if(jdata[f'Server {Server_Number}'][1]['Players'][0]):
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Players'][1], inline=False)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Players'][2], value=jdata[f'Server {Server_Number}'][1]['Players Warning'][0], inline=True)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Players'][3], value=jdata[f'Server {Server_Number}'][1]['Players Warning'][1], inline=True)
                if(jdata[f'Server {Server_Number}'][1]['Version'][0]):
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Version'][1], inline=False)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Version'][2], value=jdata[f'Server {Server_Number}'][1]['Version Warning'][0], inline=True)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Version'][3], value=jdata[f'Server {Server_Number}'][1]['Version Warning'][1], inline=True)
                if(jdata[f'Server {Server_Number}'][1]['Pastebin'][0]):
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Pastebin'][1], inline=False)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Pastebin'][2], value=jdata[f'Server {Server_Number}'][1]['Pastebin Warning'][0], inline=True)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Pastebin'][3], value=jdata[f'Server {Server_Number}'][1]['Pastebin Warning'][1], inline=True)
                if(jdata[f'Server {Server_Number}'][1]['Infomation'][0]):
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['Infomation'][1], inline=False)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Infomation'][2], value=jdata[f'Server {Server_Number}'][1]['Infomation Warning'][0].replace("%FriendlyFire%", FF1).replace("%Whitelist%", WL1).replace("%Modded%", Modded1), inline=True)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Infomation'][3], value=jdata[f'Server {Server_Number}'][1]['Infomation Warning'][1].replace("%FriendlyFire%", FF2).replace("%Whitelist%", WL2).replace("%Modded%", Modded2), inline=True)
                if(jdata[f'Server {Server_Number}'][1]['LastOnline'][0]):
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['Separate line'], value=jdata[f'Server {Server_Number}'][1]['LastOnline'][1], inline=False)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['LastOnline'][2], value=jdata[f'Server {Server_Number}'][1]['LastOnline Warning'][0], inline=True)
                    embed.add_field(name=jdata[f'Server {Server_Number}'][1]['LastOnline'][3], value=jdata[f'Server {Server_Number}'][1]['LastOnline Warning'][1], inline=True)
                embed.set_footer(text=jdata[f'Server {Server_Number}'][1]['Last Updated'].replace("%Time%", dt2.strftime('%Y-%m-%d %H:%M:%S')) + "Made by 誠誠#7773", icon_url=owner.avatar_url)
            await message.edit(embed=embed, content="")
            print(F"[Server #{Server_Number}][{dt2.strftime('%Y-%m-%d %H:%M:%S')}] 伺服器資料已更新")
            Server_Number += 1
        if(jdata['Do not change this']["Success"]):
            await asyncio.sleep(jdata['Do not change this']["Cooldown"])
        else:
            await asyncio.sleep(24)
        
bot1.run(jdata['Server 1'][0]['Discord Bot Token'])