import discord
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from player import Player
from game import Game
from database_interactions import download_player, download_players, add_player, get_player_names
from database_interactions import update_head_to_head, get_hashable_key, get_database, update_player_in_mongo
import os


'''
pip3 install discord
pip3 install "pymongo[srv]"
pip3 install python-dateutil
pip3 install datetime
'''

'''
https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
'''

load_dotenv()

#Link to basic instructions for bot ^^
starting_elo = 1500
k_factor = 20
elo_denom = 400

####################

def calc_expected_wins(player_elo , opponent_elo):
    '''
    Takes in parameters of elos and returns the players expected wins
    '''  
    expected_wins = 1/(1+10**((opponent_elo - player_elo)/elo_denom))   
    return expected_wins
    
    
def calculate_elo_changes(elo1 : int ,elo2 : int, player1Wins : bool) -> list[int]:
    '''
    Takes in the elo of each player (elo1, elo2) and if player1 wins the game. Returns array with
    the change values that should be ADDED to each players elo

    player_1_new_elo = player_1_old_elo + result[0]
    player_2_new_elo = player_2_old_elo + result[1]
    '''
    player_1_expected = calc_expected_wins(elo1,elo2)
    player_2_expected = calc_expected_wins(elo2,elo1)

    if player1Wins:
        player_1_change = k_factor * (1-player_1_expected)
        player_2_change = k_factor * (0-player_2_expected)
    else:
        player_1_change = k_factor * (0-player_1_expected)
        player_2_change = k_factor * (1-player_2_expected)
    return [player_1_change, player_2_change]
    
def output_leaderboard():
    playerList = download_players()
    tuple_list = []
    for player in playerList:
        tuple_list.append((player, player.elo))
    
    tuple_list = sort_list(tuple_list)
    
    return_string = "Current Leaderboard: \n"
    for player_tuple in tuple_list:
        player = player_tuple[0]
        return_string += str(player.name) + ": " + str(player.elo) + " (wins: "+str(player.wins)+", losses: "
        return_string += str(player.losses)+", games played: "+str(player.games_played)+") \n"
    return return_string

def sort_list(list):
    lst = len(list)
    for i in range(0, lst):
        for j in range(0, lst-i-1):
            if (list[j][1] < list[j + 1][1]):
                temp = list[j]
                list[j]= list[j + 1]
                list[j + 1]= temp
    return list



def update_player_info(player1, player2, game):
    player_1_won = game.winner == player1.name
    elo_deltas = calculate_elo_changes(player1.elo, player2.elo, player_1_won)
    player1.elo += int(elo_deltas[0])
    player2.elo += int(elo_deltas[1])
    
    if player_1_won: 
        player1.wins += 1
        player2.losses += 1
    else:
        player2.wins += 1
        player1.losses += 1
    
    player1.games_played += 1
    player2.games_played += 1




        






    

#add a game to the database by creating an instance and uploading
def add_game(winner:str, loser:str, scores:list, time: datetime):
    db = get_database()
    collection = db["Games"]
    info = {
        "date" : time,
        "winner" : winner,
        "loser" : loser,
        "winner_score" : scores[0],
        "loser_score" : scores[1]
    }
    collection.insert_one(info)
    pass

def get_hashable_key(winner: str, loser: str) -> str:
    key_list = [winner, loser]
    key_list.sort()
    return key_list[0] + "-" + key_list[1]


def update_head_to_head(winner, loser) -> str:
    key = get_hashable_key(winner, loser)
    db = get_database()
    collection = db["HeadToHead"]
    sorted_users = [winner, loser]
    sorted_users.sort()
    item = collection.find_one( {"key" : key })
    if (not item):
        #head to head record has not been established, creating one now
        if (winner == sorted_users[0]):
            #if the winner comes first in alphabetical order
            #add 1 win to user 1
            info = {
                "key" : key, 
                "user1" : sorted_users[0], 
                "user2": sorted_users[1],
                "user1wins": 1,
                "user2wins" : 0, 
            }
            collection.insert_one(info)
        else:
            #the winner comes second in alphabetical order
            info = {
                "key" : key, 
                "user1" : sorted_users[0], 
                "user2": sorted_users[1],
                "user1wins": 0,
                "user2wins" : 1, 
            }
            collection.insert_one(info)
    else: #record already exists
        if (winner == sorted_users[0]):
            collection.find_one_and_update(
                {"key" : key},
                {"$inc":
                    {"user1wins" : 1}
                }
            )
        else:
            collection.find_one_and_update(
                {"key" : key},
                {"$inc":
                    {"user2wins" : 1}
                }
            )

def display_head_to_head(player1: str, player2 : str) -> str:
    key = get_hashable_key(player1,player2)
    db = get_database()
    collection = db["HeadToHead"]
    item = collection.find_one( {"key" : key })
    if player1 == item["user1"]:
        return player1 + "-" + player2 + ": " + str(item["user1wins"]) + "-" + str(item["user2wins"])
    elif player2 == item["user1"]:
        return player1 + "-" + player2 + ": " + str(item["user2wins"]) + "-" + str(item["user1wins"])
    
    
    #return player1 + "-" + player2 + ": " + item


def game_input(date, winner, loser, winner_score, loser_score):
    game = Game(date, winner, loser, winner_score, loser_score)
    add_game(winner, loser, [winner_score, loser_score], date)
    players = [download_player(winner), download_player(loser)]
    
    update_player_info(players[0], players[1], game)
    
    update_player_in_mongo(players[0])
    update_player_in_mongo(players[1])
    
    update_head_to_head(winner, loser)

#return string the bot should send when checking stats
def get_stats(name1:str, name2=None):
    pass

def team_game_input(date, winner1, winner2, loser1, loser2, winner_score, loser_score):
    
    game = Game(date, winner1+winner2, loser1+loser2, winner_score, loser_score)
    add_game(winner1+winner2, loser1+loser2, [winner_score, loser_score], date)
    
    players = [download_player(winner1), download_player(winner2), download_player(loser1), download_player(loser2)]
    update_2player_info(players[0],players[1],players[2],players[3])
    
    for i in range(4):
        update_player_in_mongo(players[i])


def update_2player_info(winner1,winner2,loser1,loser2):
    team1_elo = (winner1.elo + winner2.elo)/2
    team2_elo = (loser1.elo + loser2.elo)/2
    
    elo_deltas = calculate_elo_changes(team1_elo,team2_elo,True)

    winner1.elo += int(elo_deltas[0]/2)
    winner2.elo += int(elo_deltas[0]/2)
    loser1.elo += int(elo_deltas[1]/2)
    loser2.elo += int(elo_deltas[1]/2)


def display_player(player_name : str):
    player_obj = download_player(player_name)
    return repr(player_obj)


# Discord input functions
#handle errors
discordBotToken = os.environ.get('discordBotToken')
helpMessage = '''**Commands:** \n
\n 
**LEADERBOARD** \n 
*“!leaderboard”* \n 
See the leaderboard of the best and worst members of Sigma United. \n 
\n 
**ADD GAME** \n 
Singles game: *"!game (winner name) (loser name) (winner goals)-(loser goals)”* \n 
Doubles game: *"!game (winner #1 name) (winner #2 name)) (loser #1 name) (loser #2 name) (winner goals)-(loser goals)”* \n
Add a new game. Input winner and loser names, and goals scored. \n 
\n 
**STATS** \n 
*“!stats (player 1) (optional player2)”* \n 
Check your stats. Add two names for head to head, and one name for your record. \n 
\n 
**NEW PLAYER** \n 
*“!newplayer (name)”* \n 
Add a new player to the fifa rankings. \n 
\n 
**HELP** \n 
*“!help”* \n 
This is your help!'''
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

    #input a fifa score
    if message.content.startswith('!game'):
        valid_players = get_player_names()
        text = message.content.split(" ")
        if len(text) != 4:
            output = 'Error in formatting the message: should be of the format "!game (winner name) (loser name) (score-score)"'
        elif text[1] not in valid_players or text[2] not in valid_players:
            output = 'Missing player: one or both of the player names are not in the database. Initialize the new player or check spelling.'
        else:
            output = f'{text[2]} got shit on!'
            scores = text[3].split("-")
            if int(scores[0]) < int(scores[1]):
                output = "Change your names and scores around: winner should come first!"
            else:
                game_input(datetime.now(), text[1], text[2], scores[0], scores[1]) #FIX
        await message.channel.send(f'`{output}`')
        #!game (winner name) (loser name) (score-score) (0,1,2)

    #input a fifa score
    if message.content.startswith('!twogame'):
        valid_players = get_player_names()
        text = message.content.split(" ")
        if len(text) != 6:
            output = 'Error in formatting the message: should be of the format "!game (winner1 name) (winner2 name) (loser1 name) (loser2 name) (score-score)"'
        elif text[1] not in valid_players or text[2] not in valid_players or text[3] not in valid_players or text[4] not in valid_players:
            output = 'Missing player: one or multiple player names are not in the database. Initialize the new player or check spelling.'
        else:
            output = "Added game!"
            scores = text[5].split("-")
            if int(scores[0]) < int(scores[1]):
                output = "Change your names and scores around: winner should come first!"
            else:
                output = team_game_input(datetime.now(), text[1], text[2], text[3], text[4], scores[0], scores[1]) #FIX
        await message.channel.send(f'`{output}`')
        #!game (winner name) (loser name) (score-score) (0,1,2)


    #get stats output
    if message.content.startswith('!stats'):
        valid_players = get_player_names()
        text = message.content.split(" ")
        if (len(text) == 2):
            #one player case
            if text[1] not in valid_players:
                output = "player not found"
            else:
                output = display_player(text[1])
        elif (len(text) == 3):
            if text[1] not in valid_players:
                output = "first player not found"
            elif text[2] not in valid_players:
                output = "second player not found"
            else:
                output = display_head_to_head(text[1], text[2])
        else:
            output = 'Error in formatting the message: should be of the format "!stats (playername) optional(playername)"'
        await message.channel.send(f'`{output}`')
        #!stats (winner name) (option: loser name)

    #get help
    if message.content.startswith('!help'):
        await message.channel.send(helpMessage)
        #!help

    #add a new player
    if message.content.startswith('!newplayer'):
        valid_players = get_player_names()
        if len(message.content.split(' ')) != 2:
            output = 'Error in formatting the message: should be of the format "!newplayer (playername)"'
        elif text[1] not in valid_players: 
            command, output = message.content.split(' ')
            add_player(output)
            output = 'Added! '+output
        else:
            output = "player already in database"
        await message.channel.send(f'`{output}`')
        #!add new player
    
    #return leaderboard
    if message.content.startswith('!leaderboard'):
        await message.channel.send(f'`{output_leaderboard()}`')
        #!leaderboard

client.run(discordBotToken)


add_player("ElieC")
add_player("IanG")
print(display_head_to_head("ElieC", "IanG"))
print(display_head_to_head("IanG", "ElieC"))