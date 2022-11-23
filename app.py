import discord 
import os
from datetime import datetime

from fifaBot.fifa_commands import bang_chance, bang_game, bang_fifahelp, bang_leaderboard
from fifaBot.fifa_commands import bang_newplayer, bang_stats, bang_teamstats, bang_twogame
from fifaBot.fifa_commands import bang_twoleaderboard, bang_newteam



discordBotToken = os.environ.get('discordBotToken')
helpMessage = '''**Commands:**
**FIFA COMMANDS**
*“!fifahelp"*
See commands for FIFA functionality

More coming soon! Talk to your local Sigma Dev!
'''
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        await message.channel.send(helpMessage)


    ####FIFA####

    if message.content.startswith('!game'):
        await message.channel.send(f'`{bang_game(message.content.split(" "))}`')

    if message.content.startswith('!twogame'):
        await message.channel.send(f'`{bang_twogame(message.content.split(" "))}`')

    if message.content.startswith('!stats'):
        await message.channel.send(f'`{bang_stats(message.content.split(" "))}`')
    
    if message.content.startswith('!teamstats'):
        await message.channel.send(f'`{bang_teamstats(message.content.split(" "))}`')

    if message.content.startswith('!fifahelp'):
        await message.channel.send(bang_fifahelp())

    if message.content.startswith('!newplayer'):
        await message.channel.send(f'`{bang_newplayer(message.content.split(" "))}`')

    if message.content.startswith('!newteam'):
        await message.channel.send(f'`{bang_newteam(message.content.split(" "))}`')
        
    if message.content.startswith('!leaderboard'):
        await message.channel.send(f'`{bang_leaderboard()}`')
    
    if message.content.startswith('!twoleaderboard'):
        await message.channel.send(f'`{bang_twoleaderboard()}`')
    
    if message.content.startswith('!chance'):
        await message.channel.send(f'`{bang_chance(message.content.split(" "))}`')

    ####FIFA####

    

client.run(discordBotToken)