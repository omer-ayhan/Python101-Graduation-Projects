import discord
import json
import asyncio
from discord.ext import commands
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix='!',intents=intents)
with open("TOKEN_KEY.json") as key:
    token_data = json.load(key)
TOKEN = token_data['TOKEN']
bot.stop_timer = True
bot.channel_name = "genelchat"

def check_cmd(msg):
    if bot.stop_timer==False:
        return
    else:
        return msg
@bot.event
async def on_ready():
    print("Pomodoro Bot Başlatılıyor...")

@bot.event
async def on_command_error(ctx, error):
    user = ctx.author.mention
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Böyle bir komut bulunmamakta {user}")

@bot.command()
async def p_başlat(ctx,s1,s2):
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    user = ctx.author.mention
    s1 = int(s1) * 60
    s2 = int(s2) * 60
    print(type(s1), type(s2))
    s1_str = int(s1/60)
    s2_str = int(s2/60)
    print(s1_str, s2_str)
    bot.stop_timer = True
    str = f"{s1_str} dakika ders\n{s2_str} dakika dinlenme {user}"
    await channel.send(str)
    print(bot.stop_timer)
    while bot.stop_timer:
        check_cmd(await asyncio.sleep(s1))
        await channel.send(check_cmd(f"Ders süresi bitti:laughing: {s2_str} dakika dinlenme vakti :sunglasses: {user}"))
        check_cmd(await asyncio.sleep(s1))
        await channel.send(check_cmd(f"Dinlenme süresi bitti:weary: {s1_str} dakika ders vakti :nerd: {user}"))

@bot.command()
async def p_durdur(ctx):
    bot.stop_timer=False
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    await channel.send(f"Pomodoro durduruldu {user}")
    
@p_başlat.error
async def pomodoro_error(ctx, error):
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    if isinstance(error, commands.MissingRequiredArgument):
        await channel.send(f"Lütfen komudu tam haliyle yazınız {user}")
    elif isinstance(error, commands.CommandInvokeError):
        await channel.send(f"Lütfen sayı giriniz {user}")
bot.run(TOKEN)