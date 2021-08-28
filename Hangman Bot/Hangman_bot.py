import discord
import json
from discord.ext import commands
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot_main = commands.Bot(command_prefix='!',intents=intents)
bot_main.channel_name="test-chat"
bot_main.guess_word="test"
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
    if args.length==1:
        channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
        user = ctx.author.mention
        # for i in list(args):
        #     str_word=str_word.join(i)
        print(args)
        if args in bot_main.guess_word:
            await channel.send("guessed")
        else:
            await channel.send("not guessed")
        
@guess.error
async def pomodoro_error(ctx, error):
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    if isinstance(error, commands.CommandInvokeError):
        await channel.send(f"Please enter only one word {user}")

bot_main.run(TOKEN)