import discord
import json
from discord.ext import commands
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot_main = commands.Bot(command_prefix='!',intents=intents)
bot_main.channel_name="test-chat"
bot_main.guess_word="test"
bot_main.lives=5
with open("TOKEN_KEY.json") as key:
    token_data = json.load(key)
TOKEN = token_data['TOKEN_HANGMAN_GAME']
@bot_main.event
async def on_ready():
    print("Hangman Bot İnitializing...")
@bot_main.event
async def on_command_error(ctx, error):
    user = ctx.author.mention
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command {user}")

@bot_main.command()
async def guess(ctx,args):
    lives_left=bot_main.lives
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    user = ctx.author.mention
    print(args)
    if args in bot_main.guess_word:
        await channel.send("guessed")
    else:
        print(lives_left)
        await channel.send("not guessed")
        # str_hang=f"`{' '*4}_____\n{' '*4}|{' '*4}|\n{' '*4}|{' '*4}\n{' '*4}|{' '*4}\n{' '*4}|{' '*4}\n{' '*4}|{' '*4}\n{' '*4}|{' '*4}\n ___|___{' '*4}`"
        str_hang=f"`{' '*4}_____\n`"
        for i in range(6):
            str_hang+=f"`{' '*2}|{' '*4}{lives_left if (lives_left<=5 and lives_left>3) else ' ' }\n`"
            lives_left-=1
        await channel.send(str_hang)
        
        
# @guess.error
# async def pomodoro_error(ctx, error):
#     user = ctx.author.mention
#     channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
#     if isinstance(error, commands.CommandInvokeError):
#         await channel.send(f"Please enter only one word {user}")

bot_main.run(TOKEN)