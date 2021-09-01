import discord
import json
import asyncio
from discord.ext import commands
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
# all commands should start with "!"
bot = commands.Bot(command_prefix='!',intents=intents)
#opening our file to read the token key
with open("TOKEN_KEY.json") as key:
    # loading all contents to a variable after opening it
    token_data = json.load(key)
# choosing oue token key
TOKEN = token_data['TOKEN_POMODORO']
# a bool to start/end timer
bot.start_times = True
bot.channel_name = "pomodoro-bot"
# a function to check if timer stopped or not for each code line
def check_cmd(msg):
    if bot.start_times==False:
        return
    else:
        return msg
@bot.event
# prints on bot launch
async def on_ready():
    print("Pomodoro Bot İnitializing...")

# a function to check errors for all commands
@bot.event
async def on_command_error(ctx, error):
    # this lets us mention the user who written the message
    user = ctx.author.mention
    # if there is an unspecified command this will be executed
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command {user}")

# a decorator for our special commands    
@bot.command()
async def p_start(ctx,s1,s2):
    # this lets us send messages to a specified channel
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    user = ctx.author.mention
    # checks if given arguments are number or not
    if s1.isnumeric() and s2.isnumeric():
        # converting to minutes from seconds
        s1 = int(s1) * 60
        s2 = int(s2) * 60
        print(type(s1), type(s2))
        s1_str = int(s1) / 60
        s2_str = int(s2) / 60
        print(s1_str, s2_str)
        # starting our timer
        bot.start_times = True
        str = f"{s1_str} minutes study time\n{s2_str} minutes break time {user}"
        await channel.send(str)
        print(bot.start_times)
        while bot.start_times:
            # using asyncio library to make our timer by giving delay with the specified value
            # check_cmd function checks if bool is still true  
            check_cmd(await asyncio.sleep(s1))
            await channel.send(check_cmd(f"Study time over:laughing: {s2_str} minutes break time :sunglasses: {user}"))
            check_cmd(await asyncio.sleep(s1))
            await channel.send(check_cmd(f"Break time over:weary: {s1_str} minutes study time :nerd: {user}"))
    else:
        await channel.send(f'Please enter all arguments as numbers {user}')

@bot.command()
# a function command to stop our timer
async def p_stop(ctx):
    bot.start_times=False
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    await channel.send(f"Pomodoro stopped {user}")
    
@p_start.error
# checks errors for that specific command
async def pomodoro_error(ctx, error):
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot.channel_name)
    # checks for any missing arguments
    if isinstance(error, commands.MissingRequiredArgument):
        await channel.send(f"Please write all arguments {user}")
# runs our with the given token key
bot.run(TOKEN)