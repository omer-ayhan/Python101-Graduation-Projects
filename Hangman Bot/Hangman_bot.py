import discord
import json
from discord.ext import commands
from discord.ext.commands.core import bot_has_permissions, has_permissions
import hangman_shape
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot_main = commands.Bot(command_prefix='!',intents=intents)
bot_main.channel_name="hangman-game"
# variable to store guess word
bot_main.game_word=""
# variable to store answer word
bot_main.guess_word=""
# attemp counter until 7
bot_main.attempt=0
#opening our file to read the token key
with open("TOKEN_KEY.json") as key:
    # loading all contents to a variable after opening it
    token_data = json.load(key)
# choosing oue token key
TOKEN = token_data['TOKEN_HANGMAN_GAME']
@bot_main.event
# prints on bot launch
async def on_ready():
    print("Hangman Bot İnitializing...")
@bot_main.event
# a function to check errors for all commands
async def on_command_error(ctx, error):
    # takes username to mention and saves it to a variable
    user = ctx.author.mention
    # if there is an unspecified command this will be executed
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command {user}")

# a decorator for our special commands    
@bot_main.command()
# to give our permissions for manipulating messages
@bot_has_permissions(manage_messages=True)
@has_permissions(manage_messages=True)
# a function to set the word to guess 
async def set_guess(ctx, word):
    # this decides which channel to send messages
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    user = ctx.author.mention
    # checks if our word written in discord's spoiler tags
    if "||" in word:
        # after remove those spoiler tags
        word=word.replace("||",'')
        # remove written message by user
        await channel.purge(limit=1)
        # written guess word has to be longer than 1 letter
        if len(word)>1:
            bot_main.game_word = word.strip()
            # temporary variable to manipulate the guess word
            bot_main.temp_word = word.strip()
            # resets guess word to prevent any conflicts
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
    # our answer has to be 1 letter
    if len(answer)==1:
        # checks if guess word is not 1 letter 
        if len(bot_main.game_word)>1:
            # checking if our user's guess is correct
            if (answer in bot_main.temp_word):
                # concatenates correct answer to answer variable
                bot_main.guess_word += answer
                print(bot_main.guess_word)
                # removes that from our temporary variable to prevent any conflicts
                bot_main.temp_word=bot_main.temp_word.replace(answer,'',1)          
                print(bot_main.temp_word)
                await channel.send(f"'{answer}' guessed one:star_struck:  {user}")
                # to check if all guesses matches the answer
                if len(bot_main.guess_word)==len(bot_main.game_word):
                    await channel.send(f"'{user} won the game :star_struck:'")
                    # resets the game
                    bot_main.game_word=""
                    bot_main.guess_word=""
                    await channel.send(f"set a new word")

            else:
                await channel.send(f"'{answer}' wrong:japanese_ogre:  {user}")
                print(bot_main.attempt)
                # if the guess is wrong, then it sends hangman shape according to the attempt number
                await channel.send(f"`{hangman_shape.HANGMAN_PICS[bot_main.attempt]}`")
                # this goes until 7
                bot_main.attempt += 1
                if bot_main.attempt==7:
                    await channel.send(f"'{user} game over:smiling_imp: '")
                    bot_main.game_word=""
                    bot_main.guess_word=""
                else:
                    # gives remaining attempts
                    await channel.send(f"{len(hangman_shape.HANGMAN_PICS)-bot_main.attempt} attempts remaining")
        else:
            await channel.send(f"please set a word to guess first {user}")
    else:
        await channel.send(f"only one word {user}")
        
# a function to check error for specific commands        
@guess.error
async def guess_error(ctx, error):
    user = ctx.author.mention
    channel = discord.utils.get(ctx.guild.text_channels, name=bot_main.channel_name)
    # checks if user entered any missing arguments
    if isinstance(error, commands.MissingRequiredArgument):
        await channel.send(f"Please give a guess {user}")
# runs our with the given token key
bot_main.run(TOKEN)