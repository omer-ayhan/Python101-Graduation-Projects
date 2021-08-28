import discord
import json
from discord.ext import commands
import hangman_shape
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot_main = commands.Bot(command_prefix='!',intents=intents)
bot_main.channel_name="test-chat"
bot_main.game_word=""
bot_main.guess_word=""
bot_main.attempt=0
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
async def set_guess(ctx, word):
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    user = ctx.author.mention
    bot_main.game_word = word.strip()
    bot_main.game_word = word.guessp()

    await channel.send(f"{user} set the word")
    
    
@bot_main.command()
async def guess(ctx,answer):
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    user = ctx.author.mention
    print(answer)
    if len(answer)==1:
        if len(bot_main.game_word)>1:
            if (answer in bot_main.guess_word):
                bot_main.guess_word += answer             
                await channel.send(f"'{answer}' guessed one:star_struck:  {user}")
                if bot_main.guess_word==bot_main.game_word:
                    await channel.send(f"'{user} won the game :star_struck:'")
                    bot_main.game_word=""
                    bot_main.guess_word=""
                    
                return
            else:
                await channel.send(f"'{answer}' wrong:japanese_ogre:  {user}")
                print(bot_main.attempt)
                await channel.send(f"`{hangman_shape.HANGMAN_PICS[bot_main.attempt]}`")
                bot_main.attempt += 1
                await channel.send(f"{7-bot_main.attempt} attempts remaining")
        else:
            await channel.send(f"please set a word to guess first {user}")
    else:
        await channel.send(f"only one word {user}")
        
        
@guess.error
async def pomodoro_error(ctx, error):
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    if isinstance(error, commands.MissingRequiredArgument):
        await channel.send(f"Please give a guess {user}")

bot_main.run(TOKEN)