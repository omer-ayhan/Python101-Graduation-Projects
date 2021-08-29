import discord
import json
from discord.ext import commands
from discord.ext.commands.core import bot_has_permissions, has_permissions
import hangman_shape
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot_main = commands.Bot(command_prefix='!',intents=intents)
bot_main.channel_name="hangman-game"
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
@bot_has_permissions(manage_messages=True)
@has_permissions(manage_messages=True)
async def set_guess(ctx, word):
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    user = ctx.author.mention
    if "||" in word:
        word=word.replace("||",'')
        await channel.purge(limit=1)
        if len(word)>1:
            bot_main.game_word = word.strip()
            bot_main.temp_word = word.strip()
            bot_main.guess_word = ""
            print(bot_main.game_word)
            await channel.send(f"{user} set a new word")
        else:
            await channel.send(f"{user} the word needs to be longer")
    else:
        await channel.send(f"Please set your word with spoiler tags(`||your message||`){user}")

    
    
@bot_main.command()
async def guess(ctx,answer):
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    user = ctx.author.mention
    print(answer)
    if len(answer)==1:
        if len(bot_main.game_word)>1:
            if (answer in bot_main.temp_word):
                bot_main.guess_word += answer
                print(bot_main.guess_word)
                bot_main.temp_word=bot_main.temp_word.replace(answer,'',1)          
                print(bot_main.temp_word)
                await channel.send(f"'{answer}' guessed one:star_struck:  {user}")
                if len(bot_main.guess_word)==len(bot_main.game_word):
                    await channel.send(f"'{user} won the game :star_struck:'")
                    bot_main.game_word=""
                    bot_main.guess_word=""
                    await channel.send(f"set a new word")

            else:
                await channel.send(f"'{answer}' wrong:japanese_ogre:  {user}")
                print(bot_main.attempt)
                await channel.send(f"`{hangman_shape.HANGMAN_PICS[bot_main.attempt]}`")
                bot_main.attempt += 1
                if bot_main.attempt==7:
                    await channel.send(f"'{user} game over:smiling_imp: '")
                    bot_main.game_word=""
                    bot_main.guess_word=""
                else:
                    await channel.send(f"{len(hangman_shape.HANGMAN_PICS)-bot_main.attempt} attempts remaining")
        else:
            await channel.send(f"please set a word to guess first {user}")
    else:
        await channel.send(f"only one word {user}")
        
        
@guess.error
async def guess_error(ctx, error):
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    if isinstance(error, commands.MissingRequiredArgument):
        await channel.send(f"Please give a guess {user}")

bot_main.run(TOKEN)