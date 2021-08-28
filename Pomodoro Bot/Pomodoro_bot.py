import discord
import json
import asyncio
from discord.ext import commands
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix='!',intents=intents)
with open("TOKEN_KEY.json") as key:
    token_data = json.load(key)
TOKEN = token_data['TOKEN_POMODORO']
bot.start_times = True
bot.channel_name = "pomodoro-bot"

def check_cmd(msg):
    if bot.start_times==False:
        return
    else:
        return msg
@bot.event
async def on_ready():
    print("Pomodoro Bot İnitializing...")

@bot.event
async def on_command_error(ctx, error):
    user = ctx.author.mention
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command {user}")

@bot.command()
async def p_start(ctx,s1,s2):
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    user = ctx.author.mention
    s1 = int(s1) * 60
    s2 = int(s2) * 60
    print(type(s1), type(s2))
    s1_str = int(s1/60)
    s2_str = int(s2/60)
    print(s1_str, s2_str)
    bot.start_times = True
    str = f"{s1_str} minutes study time\n{s2_str} minutes break time {user}"
    await channel.send(str)
    print(bot.start_times)
    while bot.start_times:
        check_cmd(await asyncio.sleep(s1))
        await channel.send(check_cmd(f"Study time over:laughing: {s2_str} minutes break time :sunglasses: {user}"))
        check_cmd(await asyncio.sleep(s1))
        await channel.send(check_cmd(f"Break time over:weary: {s1_str} minutes study time :nerd: {user}"))

@bot.command()
async def p_stop(ctx):
    bot.start_times=False
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    await channel.send(f"Pomodoro stopped {user}")
    
@p_start.error
async def pomodoro_error(ctx, error):
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    if isinstance(error, commands.MissingRequiredArgument):
        await channel.send(f"Please write all arguments {user}")
    elif isinstance(error, commands.CommandInvokeError):
        await channel.send(f"Please enter all arguments as numbers {user}")
bot.run(TOKEN)