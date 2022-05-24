#導入 模組
import discord
import discord  #導入Discord.py的專案
from discord.ext import commands  #導入指令
import asyncio
from datetime import datetime,timezone,timedelta
intents = discord.Intents.all()

bot1 = commands.Bot(command_prefix='\\|/', intents = intents)

@bot1.event
async def on_ready():
    counter = 0
    await bot1.change_presence(status=discord.Status.idle)
    await bot1.change_presence(activity=discord.Game(name="You.", type=3))
    if counter == 0:
        print(f'＝＝＝已登入＝＝＝')
        print(f'《 {bot1.user} 》上線了')
        print(f'目前在的群組有 {bot1.guilds}')
        print(f'＝＝＝已登入＝＝＝\n')
        counter = 1
    await bot2.start('Nzg5ODA5OTY0NjkyNjY4NDU2.X93d2Q.tZWbLjX2VLY5jJoGKeoW9bcp5DA')

bot2 = commands.Bot(command_prefix='\|/', intents = intents)

@bot2.event
async def on_ready():
    counter = 0
    await bot2.change_presence(status=discord.Status.offline)
    if counter == 0:
        print(f'＝＝＝已登入＝＝＝')
        print(f'《 {bot2.user} 》上線了')
        print(f'目前在的群組有 {bot2.guilds}')
        print(f'＝＝＝已登入＝＝＝\n')
        counter = 1
    await bot3.start('Nzg5ODEwMzU2NzA4MzExMDUw.X93eNw.5dDvMsviXYsRurr8zlxEVTlpqUk')

bot3 = commands.Bot(command_prefix='\|/', intents = intents)

@bot3.event
async def on_ready():
    counter = 0
    await bot3.change_presence(status=discord.Status.offline)
    if counter == 0:
        print(f'＝＝＝已登入＝＝＝')
        print(f'《 {bot3.user} 》上線了')
        print(f'目前在的群組有 {bot3.guilds}')
        print(f'＝＝＝已登入＝＝＝\n')
        counter = 1
    bot1.loop.create_task(RAINBOW())

#指令 - guild - 伺服器相關信息
@bot1.command()
async def guild(ctx):
    print(f'【指令】〔{ctx.author}〕 輸入 [guild]')
    await ctx.message.delete()
    guild = ctx.message.guild
    guild_info = discord.Embed(title=F"{guild.name}", description="[點此到達伺服器頭像連結](%s)" % guild.icon_url, color=0xd08a2b)
    guild_info.set_thumbnail(url=F"{guild.icon_url}")
    guild_info.add_field(name="名稱", value=F"{guild.name}", inline=True)
    guild_info.add_field(name="擁有者", value=F"{guild.owner}", inline=False)
    guild_info.add_field(name="設定地區", value=F"{guild.region}", inline=True)
    guild_info.add_field(name="創建日期", value=F"{guild.created_at}", inline=False)
    guild_info.add_field(name="ID", value=F"{guild.id}", inline=True)
    guild_info.add_field(name="目前成員數量", value=F"{guild.member_count}", inline=False)
    guild_info.set_footer(text=F"此指令由 {ctx.author} 輸入 • ", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=guild_info)

#指令 -info - 使用者相關信息
@bot1.command()
async def info(ctx, member: discord.Member=None):
    print(f'【指令】〔{ctx.author}〕 輸入 [info]')
    author = ctx.message.author
    await ctx.message.delete()
    if not member:
        member = ctx.message.author
    info = discord.Embed(title=F"{member}", description="[點此到達頭像連結](%s)" % member.avatar_url, color=0xd08a2b)
    info.set_thumbnail(url=F"{member.avatar_url}")
    info.add_field(name="使用者名稱", value=F"{member.name}", inline=True)
    if str(member.status) == 'online':
        info.add_field(name="目前狀態", value=F"線上", inline=False)
    elif str(member.status) == 'offline':
        info.add_field(name="目前狀態", value=F"離線", inline=False)
    elif str(member.status) == 'idle':
        info.add_field(name="目前狀態", value=F"閒置", inline=False)
    elif str(member.status) == 'dnd':
        info.add_field(name="目前狀態", value=F"請勿打擾", inline=False)
    else:
        info.add_field(name="目前狀態", value=F"無法得知", inline=False)
    if member.activity == None:
        info.add_field(name="目前狀態消息", value="無法取得 或 沒有", inline=True)
    else:
        info.add_field(name="目前狀態消息", value=F"{member.activity}", inline=True)
    time = str(member.created_at)
    loc = time.rfind('.')
    ttime = time[:loc]
    info.add_field(name="此帳號創建日期", value=F"{ttime}", inline=False)
    join = str(member.joined_at)
    loc = join.rfind('.')
    jjoin = join[:loc]
    info.add_field(name="此帳號加入此群日期", value=F"{jjoin}", inline=True)
    roles = member.roles
    info.add_field(name="在此群擁有的所有身分組", value=F",".join([role.mention for role in roles]), inline=False)
    if member.bot is True:
        info.add_field(name="使用者是否為機器人", value="是機器人", inline=True)
    else:
        info.add_field(name="使用者是否為機器人", value="不是機器人", inline=True)
    info.add_field(name="使用者ID", value=F"{member.id}", inline=False)
    info.set_footer(text=F"此指令由 {author} 輸入 • ", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=info)

#＝＝＝＝＝＝＝＝＝＝＝＝＝＝ 定時執行 ＝＝＝＝＝＝＝＝＝＝＝＝＝＝
async def RAINBOW():
    Zircon = bot1.get_guild(892799334289145896).get_member(223010788259004416)
    myrole = bot1.get_guild(892799334289145896).get_role(914842849227460618)
    Bot2role = bot2.get_guild(892799334289145896).get_role(896295716216008734)
    Bot3role = bot3.get_guild(892799334289145896).get_role(896295716216008734)
    colours = [0xFF0000, 0xFF5E00, 0xFFFB00, 0x62FF00, 0x00CCFF, 0x0800FF, 0x4800FF]
    i = 0
    a = 0
    while not bot1.is_closed():
        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
        dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
        if str(Zircon.status) != 'offline':
            now = dt2.strftime('%Y-%m-%d %H:%M:%S')
            if(a <= 25):
                await Bot2role.edit(colour=discord.Colour(colours[i]))
            else:
                await Bot3role.edit(colour=discord.Colour(colours[i]))
            print(f'[{now}] ZirconZer0 身分組改顏色拉!!! {colours[i]}\n')
            if(i == 6):
                i = 0
            else:
                i = i + 1

            if(a == 50):
                a = 0
            else:
                a = a + 1
            #await myrole.edit(colour=discord.Colour(colours[i]))
            #print(f'[{now}] 我的身分組改顏色拉!!! {colours[i]}\n\n')
        await asyncio.sleep(5)

async def MyRole():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    myrole = bot1.get_guild(892799334289145896).get_role(914842849227460618)
    role = bot1.get_guild(892799334289145896).get_role(896295716216008734)
    while not bot1.is_closed():
        now = dt2.strftime('%Y-%m-%d %H:%M:%S')
        await bot1.change_presence(activity=discord.Activity(name='你', type=discord.ActivityType.watching))
        print(f'[{now}] ZirconZer0 身分組改顏色拉!!!\n')
        await asyncio.sleep(5)

bot1.run('Nzg5ODEwNDE4Mjg4ODIwMjI2.X93eRQ.ZpnOtP5P43V9H2EzQqMCzZQHhOM')