from .player import Player, Team
from datetime import datetime
from pymongo import MongoClient

starting_elo = 1500

def get_database():

   '''
   MongoDB bot user:
   username: fifaBot
   password: UlG5lHLkhVEhul79
   CONNECTION_STRING: "mongodb+srv://fifaBot:UlG5lHLkhVEhul79@fifa-scores.qdj1pi4.mongodb.net/?retryWrites=true&w=majority"
   ''' 
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://fifaBot:UlG5lHLkhVEhul79@fifa-scores.qdj1pi4.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   return client['Fifa-Scores']
  
def get_hashable_key(winner: str, loser: str) -> str:
    key_list = [winner, loser]
    key_list.sort()
    return key_list[0] + "-" + key_list[1]


def download_player(name: str) -> Player:
    #Takes in name of player as a string and returns that player object or throws exception
    db = get_database()
    collection = db['Players']
    item = collection.find_one( { "name" : name} )
    result = Player(item["name"], int(item["elo"]), int(item["wins"]), int(item["losses"]), int(item["games_played"]), int(item["goals_for"]),\
         int(item["goals_against"]), int(item["goal_differential"]), int(item["two_wins"]), int(item["two_losses"]), int(item["two_games_played"]))
    return result

def download_team(player1:str, player2:str) -> Team:
    db = get_database()
    collection = db['Teams']
    key = get_hashable_key(player1, player2)
    item = collection.find_one( {"key" : key })
    result = Team(
        item["player1"], item["player2"], item["elo"], item["wins"], item["losses"], item["key"], 
            item["games_played"]
    )
    return result

def download_players() -> list[Player]:
    result = []
    db = get_database()
    collection = db["Players"]
    items = collection.find()
    for item in items:
        player_object = Player(item["name"], int(item["elo"]), int(item["wins"]), int(item["losses"]), int(item["games_played"]), int(item["goals_for"]),\
             int(item["goals_against"]), int(item["goal_differential"]), int(item["two_wins"]), int(item["two_losses"]), int(item["two_games_played"]))
        result.append(player_object)
    return result

#add a player to the database: create a player instance and add it to database
def add_player(player_name:str) -> None:
    db = get_database()
    collection = db["Players"]
    info = {
        "name" : player_name,
        "wins" : 0,
        "elo" : starting_elo,
        "losses" : 0,
        "games_played" : 0,
        "goals_for" : 0,
        "goals_against" : 0,
        "goal_differential" : 0,
        "two_wins" : 0,
        "two_losses" : 0,
        "two_games_played" : 0
    }
    collection.insert_one(info)

def add_team(player1: str, player2:str ) -> None:
    db = get_database()
    collection = db["Teams"]
    info = {
        "player1" : player1,
        "player2" : player2,
        "key" : get_hashable_key(player1, player2),
        "elo" : starting_elo,
        "wins" : 0,
        "losses" : 0,
        "games_played" : 0
    }
    collection.insert_one(info)


def get_player_names() -> set[str]:
    result = set()
    db = get_database()
    collection = db["Players"]
    players = collection.find()
    for player in players:
        result.add(player["name"])
    return result

def get_team_keys() -> set[str]:
    result = set()
    db = get_database()
    collection = db["Teams"]
    teams = collection.find()
    for team in teams:
        result.add(team["key"])
    return result

def update_head_to_head(winner, loser) -> None:
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

def update_twos_head_to_head(winners: list[str], losers: list[str]) -> None:
    db = get_database()
    collection = db["HeadToHead"]
    winner_key = get_hashable_key(winners[0], winners[1])
    loser_key = get_hashable_key(losers[0], losers[1])
    sorted_teams = [winner_key, loser_key]
    sorted_teams.sort()
    key = get_hashable_key(winner_key, loser_key)
    item = collection.find_one( {"key" : key})
    if (not item):
        if (sorted_teams[0] == winner_key):
            info = {
                "key" : key,
                "team1" : sorted_teams[0],
                "team2" : sorted_teams[1],
                "team1wins" : 1,
                "team2wins" : 0
            }
            collection.insert_one(info)
        else:
            info = {
                "key" : key,
                "team1" : sorted_teams[0],
                "team2" : sorted_teams[1],
                "team1wins" : 0,
                "team2wins" : 1
            }
            collection.insert_one(info)
    else:
        if (sorted_teams[0] == winner_key):
            collection.find_one_and_update(
                {"key" : key},
                {"$inc":
                    {"team1wins" : 1}
                }
            )
        else:
            collection.find_one_and_update(
                {"key" : key},
                {"$inc":
                    {"team2wins" : 1}
                }
            )


#add a game to the database by creating an instance and uploading
def add_game(winner:str, loser:str, scores:list, time: datetime) -> None:
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

def add_twogame(winner1:str, winner2:str, loser1:str, loser2: str, time:datetime, scores:list[int]) -> None:
    db = get_database()
    collection = db["TwoPlayerGames"]
    winners = get_hashable_key(winner1, winner2)
    losers = get_hashable_key(loser1, loser2)
    info = {
        "date" : time,
        "winners" : winners,
        "losers" : losers,
        "winner_score" : scores[0],
        "loser_score" : scores[1]
    }
    collection.insert_one(info)

def update_players_in_mongo(players: list[Player]) -> None: #Opportunities to Multithread
    db = get_database()
    collection = db["Players"]
    for player in players:
        collection.find_one_and_update(
            {"name" : player.name}, 
            {"$set" : { 
                "elo" : player.elo, 
                "games_played" : player.games_played,
                "wins" : player.wins,
                "losses" : player.losses,
                "goals_for" : player.goals_for,
                "goals_against" : player.goals_against,
                "goal_differential" : player.goal_differential,
                "two_wins" : player.two_wins,
                "two_losses" : player.two_losses,
                "two_games_played" : player.two_games_played
            }}
        )

def update_teams_in_mongo(teams: list[Team]) -> None: #Opportunities to Multithread
    db = get_database()
    collection = db["Teams"]
    for team in teams:
        collection.find_one_and_update(
            {"key" : team.key},
            { "$set" : {
                "elo" : team.elo,
                "games_played" : team.games_played,
                "wins" : team.wins,
                "losses" : team.losses
            }}
        )
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()