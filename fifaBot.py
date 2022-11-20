import discord
from pymongo import MongoClient
from pymongo_get_database import get_database
from datetime import datetime

'''
pip3 install discord
pip3 install "pymongo[srv]"
pip3 install python-dateutil
pip3 install datetime
'''

'''
https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
'''

#Link to basic instructions for bot ^^
starting_elo = 1500
k_factor = 10
elo_denom = 400

#Player & Game Class
class Player:
    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of Player.")
        return super().__new__(cls)

    def __init__(self, name, elo, wins, losses, games_played):
        print("2. Initialize the new instance of Player.")
        self.name = name
        self.elo = elo
        self.wins = wins
        self.losses = losses
        self.games_played = games_played
        
    def get_record(self):
        return [self.wins, self.losses]

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, elo={self.elo})"

class Game:
    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of Game.")
        return super().__new__(cls)

    def __init__(self, date, winner, loser, winner_score, loser_score, when_won):
        print("2. Initialize the new instance of Game.")
        self.date = date # date 'MM/DD/YYYY'
        self.winner = winner #'player_name'
        self.loser = loser #'player_name'
        self.winner_score = winner_score
        self.loser_score = loser_score
        self.time_period = when_won #regular-0, et-1, penalties-2 (add 1 goal to winning team for pens)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(date={self.date}, winner={self.winner}, loser={self.loser})"

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
        tuple_list.append(player, player.elo)
    
    tuple_list = sort_list(tuple_list)
    
    return_string = "Current Leaderboard: \n"
    for player_tuple in tuple_list:
        player = player_tuple[0]
        return_string += str(player.name) + ": " + str(player.elo) + " (wins: "+str(player.wins)+", losses: "+str(player.losses)+", games played: "+str(player.games_played)+" \n"
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
    player1.elo += elo_deltas[0]
    player2.elo += elo_deltas[1]
    
    if player_1_won: 
        player1.wins += 1
        player2.losses += 1
    else:
        player2.wins += 1
        player1.losses += 1
    
    player1.games_played += 1
    player2.games_played += 1


def download_player(name: str) -> Player:
    #Takes in name of player as a string and returns that player object or throws exception
    db = get_database()
    collection = db['Players']
    item = collection.find_one( { "name" : name} )
    result = Player(item["name"], int(item["elo"]), int(item["wins"]), int(item["losses"]), int(item["games_played"]))
    return result

def download_players() -> list[Player]:
    result = []
    db = get_database()
    collection = db["Players"]
    items = collection.find()
    for item in items:
        player_object = Player(item["name"], int(item["elo"]), int(item["wins"]), int(item["losses"]), int(item["games_played"]))
        result.append(player_object)
    return result

def get_player_names() -> set[str]:
    result = set()
    db = get_database()
    collection = db["Players"]
    players = collection.find()
    for player in players:
        result.add(player["name"])
    return result
        

def update_player_in_mongo(player :Player) -> None:
    db = get_database()
    collection = db["Players"]
    collection.find_one_and_update(
        {"name" : player.name}, 
        {"$set" : { 
            "elo" : player.elo, 
            "games_played" : player.games_played,
            "wins" : player.wins,
            "losses" : player.losses
        }}
    )



#add a player to the database: create a player instance and add it to database
def add_player(player_name:str) -> None:
    db = get_database()
    collection = db["Players"]
    info = {
        "name" : player_name,
        "wins" : 0,
        "elo" : starting_elo,
        "losses" : 0,
        "games_played" : 0
    }
    collection.insert_one(info)
    

#add a game to the database by creating an instance and uploading
def add_game(winner:str, loser:str, scores:list[int], endtime:int, time: datetime):
    db = get_database()
    collection = db["Games"]
    info = {
        "date" : time,
        "winner" : winner,
        "loser" : loser,
        "time_period" : endtime,
        "winner_score" : scores[0],
        "loser_score" : scores[1]
    }
    collection.insert_one(info)
    pass

def game_input(date, winner, loser, winner_score, loser_score, time_period):
    game = Game(date, winner, loser, winner_score, loser_score, time_period)
    add_game(winner, loser, [winner_score, loser_score], time_period, date)
    players = [download_player(winner), download_player(loser)]
    update_player_info(players[0], players[1], game)
    update_player_in_mongo(players[0])
    update_player_in_mongo(players[1])

#return string the bot should send when checking stats
def get_stats(name1:str, name2=None):
    pass


'''

# Discord input functions
#handle errors
discordBotToken = ''
helpMessage = 'Commands: \n\n LEADERBOARD \n “!leaderboard” \n See the leaderboard of the best and worst members of Sigma United. \n \n ADD GAME \n "!game (winner name) (loser name) (winner goals)-(loser goals) (game_ended)” \n Add a new game. Input winner and loser names, goals scored, and game_ended time: 0 if it ended in regulation, 1 if it ended in extra time, and 2 if it ended in penalty kicks. \n \n STATS \n “!stats (player 1) (optional player2)” \n Check your stats. Add two names for head to head, and one name for your record. \n \n NEW PLAYER \n “!newplayer (name)” \n Add a new player to the fifa rankings. \n \n HELP \n “!help” \n This is your help!'
client = discord.Client();

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
        if len(text) != 5:
            output = 'Error in formatting the message: should be of the format "!game (winner name) (loser name) (score-score) (0,1,2)"'
        elif text[1] not in valid_players or text[2] not in valid_players:
            output = 'Missing player: one or both of the player names are not in the database. Initialize the new player or check spelling.'
        elif text[4] not in (0, 1, 2):
            output = 'Error in formatting the message: should be of the format "!game (winner name) (loser name) (score-score) (0,1,2)"'
        else:
            output = "Added game!"
        game_input(text[1], text[2], [text[3].split("-")], text[4], datetime.now) #FIX
        await message.channel.send(output)
        #!game (winner name) (loser name) (score-score) (0,1,2)

    #get stats output
    if message.content.startswith('!stats'):
        valid_players = get_player_names()
        text = message.content.split(" ")
        if len(text) != 2 or len(text) != 3:
            output = 'Error in formatting the message: should be of the format "!stats (name1) (option: name2)"'
        else:
            name1 = text[1]
            if len(text) == 3:
                name2 = text[2]
            else:
                name2 = None
            
            if text[1] not in valid_players or text[2] not in valid_players.add(None):
                output = 'Missing player: one or both of the player names are not in the database. Initialize the new player or check spelling.'
            else:
                output = get_stats(name1, name2)   
        await message.channel.send(output)
        #!stats (winner name) (option: loser name)

    #get help
    if message.content.startswith('!help'):
        await message.channel.send(helpMessage)
        #!help

    #add a new player
    if message.content.startswith('!newplayer'):
        if len(message.content.split(' ')) != 2:
            output = 'Error in formatting the message: should be of the format "!newplayer (playername)"'
        else: 
            command, output = message.content.split(' ')
            add_player(output)
        await message.channel.send(f'Added! {output}')
        #!add new player
    
    #return leaderboard
    if message.content.startswith('!leaderboard'):
        await message.channel.send(output_leaderboard())
        #!leaderboard

#client.run(discordBotToken)

'''
