import discord 
import os
from datetime import datetime
from fifaBot.player import Player, Team
from fifaBot.fifaBot import game_input, team_game_input, display_player, output_twoleaderboard
from fifaBot.fifaBot import display_head_to_head, output_leaderboard, chance, chance_teams
from fifaBot.fifaBot import probability_to_moneyline, display_team, display_twos_head_to_head
from fifaBot.database_interactions import download_player, get_player_names, get_team_keys, get_hashable_key
from fifaBot.database_interactions import add_player, add_team, download_team

from fifaBot.fifa_commands import bang_chance, bang_game, bang_fifahelp, bang_leaderboard
from fifaBot.fifa_commands import bang_newplayer, bang_stats, bang_teamstats, bang_twogame
from fifaBot.fifa_commands import bang_twoleaderboard, bang_newteam



discordBotToken = os.environ.get('discordBotToken')
helpMessage = '''**Commands:**
**FIFA COMMANDS**
*“!fifahelp*
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
        await message.channel.send(f'`{helpMessage}`')



    ####FIFA####

    #input a fifa score
    if message.content.startswith('!game'):
        await message.channel.send(f'`{bang_game(message.content.split(" "))}`')
        # valid_players = get_player_names()
        # text = message.content.split(" ")
        # if len(text) != 4:
        #     output = 'Error in formatting the message: should be of the format "!game (winner name) (loser name) (score-score)"'
        # elif text[1] not in valid_players or text[2] not in valid_players:
        #     output = 'Missing player: one or both of the player names are not in the database. Initialize the new player or check spelling.'
        # else:
        #     scores = text[3].split("-")
        #     if int(scores[0]) < int(scores[1]):
        #         output = "Change your names and scores around: winner should come first!"
        #     else:
        #         game_input(datetime.now(), text[1], text[2], int(scores[0]), int(scores[1])) #FIX
        #         output = f'{text[2]} got shit on!'
        # await message.channel.send(f'`{output}`')
        # #!game (winner name) (loser name) (score-score) (0,1,2)

    #input a fifa score
    if message.content.startswith('!twogame'):
        await message.channel.send(f'`{bang_twogame(message.content.split(" "))}`')
        # valid_players = get_player_names()
        # valid_teams = get_team_keys()
        # text = message.content.split(" ")
        # if len(text) != 6:
        #     output = 'Error in formatting the message: should be of the format "!game (winner1 name) (winner2 name) (loser1 name) (loser2 name) (score-score)"'
        # elif text[1] not in valid_players or text[2] not in valid_players or text[3] not in valid_players or text[4] not in valid_players:
        #     output = 'Missing player: one or multiple player names are not in the database. Initialize the new player or check spelling.'
        # else:
        #     winner_key = get_hashable_key(text[1], text[2])
        #     loser_key = get_hashable_key(text[3], text[4])
        #     if (loser_key not in valid_teams):
        #         output = "losing team not recognized. initialize with !newteam"
        #     elif (winner_key not in valid_teams):
        #         output = "winning team not recognized. initialize with !newteam"
        #     else:
        #         scores = text[5].split("-")
        #         if int(scores[0]) < int(scores[1]):
        #             output = "Change your names and scores around: winner should come first!"
        #         else:
        #             team_game_input(datetime.now(), text[1], text[2], text[3], text[4], scores[0], scores[1]) #FIX
        #             output = f'lmao {text[3]} and {text[4]} are trash'
        # await message.channel.send(f'`{output}`')
        #!game (winner name) (loser name) (score-score) (0,1,2)


    #get stats output
    if message.content.startswith('!stats'):
        await message.channel.send(f'`{bang_stats(message.content.split(" "))}`')
        # valid_players = get_player_names()
        # text = message.content.split(" ")
        # if (len(text) == 2):
        #     #one player case
        #     if text[1] not in valid_players:
        #         output = "player not found"
        #     else:
        #         output = display_player(text[1])
        # elif (len(text) == 3):
        #     if text[1] not in valid_players:
        #         output = "first player not found"
        #     elif text[2] not in valid_players:
        #         output = "second player not found"
        #     else:
        #         output = display_head_to_head(text[1], text[2])
        # else:
        #     output = 'Error in formatting the message: should be of the format "!stats (playername) optional(playername)"'
        # await message.channel.send(f'`{output}`')
        #!stats (winner name) (option: loser name)

    if message.content.startswith('!teamstats'):
        await message.channel.send(f'`{bang_teamstats(message.content.split(" "))}`')
        # text = message.content.split(" ")
        # valid_teams = get_team_keys()
        # if (len(text) not in [3, 5]):
        #     output = 'Error in formatting the message: should be of the format "!stats (playername) (playername) optional(playername playername)"'
        # else:
        #     if (len(text) == 3):
        #         #single team stats
        #         key = get_hashable_key(text[1], text[2])
        #         if (key not in valid_teams):
        #             output = "Team not initialized. try !newteam"
        #         else:
        #             team = download_team(text[1], text[2])
        #             output = display_team(team)
        #     else:
        #         #double team head-to-head
        #         key1 = get_hashable_key(text[1], text[2])
        #         key2 = get_hashable_key(text[3], text[4])
        #         if (key1 not in valid_teams):
        #             output = "first team not initialized. try !newteam"
        #         elif (key2 not in valid_teams):
        #             output = "second team not initalized. try !newteam"
        #         else:
        #             team1 = download_team(text[1], text[2])
        #             team2 = download_team(text[3], text[4])
        #             output = display_twos_head_to_head(team1, team2)

        # await message.channel.send(f'`{output}`')

    #get help
    if message.content.startswith('!fifahelp'):
        await message.channel.send(bang_fifahelp)
        #!help

    #add a new player
    if message.content.startswith('!newplayer'):
        await message.channel.send(f'`{bang_newplayer(message.content.split(" "))}`')
        # valid_players = get_player_names()
        # text = message.content.split(' ')
        # if len(text) != 2:
        #     output = 'Error in formatting the message: should be of the format "!newplayer (playername)"'
        # elif text[1] not in valid_players: 
        #     command, output = message.content.split(' ')
        #     add_player(output)
        #     output = 'Added! '+output
        # else:
        #     output = "player already in database"
        # await message.channel.send(f'`{output}`')
        #!add new player
    
    if message.content.startswith('!newteam'):
        await message.channel.send(f'`{bang_newteam(message.content.split(" "))}`')
        # valid_teams = get_team_keys()
        # valid_players = get_player_names()
        # text = message.content.split(' ')
        # if (len(text) != 3):
        #     output = 'Error in formatting the message: should be of the format "!newplayer (player1) (player2)"'
        # else:
        #     player1 = text[1]
        #     player2 = text[2]
        #     if (player1 not in valid_players):
        #         output = "First player not recognized. Initialize them first with !newplayer"
        #     elif (player2 not in valid_players):
        #         output = "Second player not recognized. Initialize them first with !newplayer"
        #     else:
        #         key = get_hashable_key(player1, player2)
        #         if (key not in valid_teams):
        #             add_team(player1, player2)
        #             output = "Added!" + player1 + ", " + player2
        #         else:
        #             output = "Team already initialized"
            
        # await message.channel.send(f'`{output}`')
        
    
    #return leaderboard
    if message.content.startswith('!leaderboard'):
        await message.channel.send(f'`{bang_leaderboard}`')
        #!leaderboard
    
    if message.content.startswith('!twoleaderboard'):
        await message.channel.send(f'`{bang_twoleaderboard()}`')
    
    if message.content.startswith('!chance'):
        await message.channel.send(f'`{bang_chance(message.content.split(" "))}`')
        # text = message.content.split(' ')
        # valid_players = get_player_names()
        # valid_teams = get_team_keys()
        # if (len(text) not in [3,5]):
        #     output = 'Error in formatting the message, should be of the format !chance (lpayer1name) (player2name)'
        # else:
        #     if (len(text) == 3):
        #         player1: Player = download_player(text[1])
        #         player2: Player = download_player(text[2])
        #         if (player1.name not in valid_players):
        #             output = "first player not recognized"
        #         elif (player2.name not in valid_players):
        #             output = "second player not recognized"
        #         else:
        #             p, q = chance(player1, player2)
        #             p_ml, q_ml = probability_to_moneyline(p), probability_to_moneyline(q)
        #             output = f'{"Names" : ^15}|{"P(win)": ^10}|{"ML": ^10}\n'
        #             output += "-" * 15 + "|" + "-"*10 + "|" + "-" * 10 + "\n"
        #             output += f'{player1.name : <15}{round((p*100),1): >9}%|{"+" + str(p_ml) if p_ml > 0 else str(p_ml): >10}\n'
        #             output += f'{player2.name : <15}{round((q*100),1): >9}%|{"+" + str(q_ml) if q_ml > 0 else str(q_ml): >10}'
        #     else:
        #         team1key = get_hashable_key(text[1], text[2])
        #         team2key = get_hashable_key(text[3], text[4])
        #         if (team1key not in valid_teams):
        #             output = "first team not recognized. try initializing with !newteam"
        #         elif (team2key not in valid_teams):
        #             output = "second team not recognized. try initializing with !newteam"
        #         else:
        #             team1: Team = download_team(text[1], text[2])
        #             team2: Team = download_team(text[3], text[4])
        #             p,q  = chance_teams(team1, team2)
        #             p_ml, q_ml = probability_to_moneyline(p), probability_to_moneyline(q)
        #             output = f'{"Names" : ^15}|{"P(win)": ^10}|{"ML": ^10}\n'
        #             output += "-" * 15 + "|" + "-"*10 + "|" + "-" * 10 + "\n"
        #             output += f'{team1.player1 + "-" + team1.player2 : <15}{round((p*100),1): >9}%|{"+" + str(p_ml) if p_ml > 0 else str(p_ml): >10}\n'
        #             output += f'{team2.player1 + "-" + team2.player2 : <15}{round((q*100),1): >9}%|{"+" + str(q_ml) if q_ml > 0 else str(q_ml): >10}'

        # await message.channel.send(f'`{output}`')
            
    ####FIFA####

    

client.run(discordBotToken)