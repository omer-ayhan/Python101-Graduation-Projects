# Python101 Graduation Projects
This is a repository for graduation projects. You can find various projects for your needs which all done with python

:triangular_flag_on_post: Table of Contents
-----
* [<b>Table of Contents</b>](https://github.com/omer-ayhan/Python101-Graduation-Projects#triangular_flag_on_post-table-of-contents)
* [<b>Setup for Bots</b>](https://github.com/omer-ayhan/Python101-Graduation-Projects#robot-setup-for-bots)
* [<b>Features for Bots</b>](https://github.com/omer-ayhan/Python101-Graduation-Projects#sparkles-features)

:robot: Setup for Bots
----
* required packages for discord bots:
  * Hangman Bot: `discord.py, json(built-in),discord.ext`
  * Pomodoro Bot: `discord.py, json(built), asyncio, discord.ext`
* create a file named `TOKEN_KEY.json` and keep it in the root directory of your project
* create key name and put your token key that you've taken from discord developer portal inside key value
* don't forget specify that key name inside whichever script you want to use

:sparkles: Features
----
## Pomodoro Bot :
* `!p_start study break` : lets us start pomodoro by specifying study and break time in minutes
*  `!p_stop` : stops the pomodoro timer
## Hangman Bot :
* `!set_guess word` : sets a word to guess which also starts the game
* `!guess letter` : helps us to guess by only giving a letter 
