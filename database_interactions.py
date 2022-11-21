from player import Player
from pymongo_get_database import get_database
from fifaBot import starting_elo
from datetime import datetime
from pymongo import MongoClient

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
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()



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

def get_hashable_key(winner: str, loser: str) -> str:
    key_list = [winner, loser]
    key_list.sort()
    return key_list[0] + "-" + key_list[1]

def get_player_names() -> set[str]:
    result = set()
    db = get_database()
    collection = db["Players"]
    players = collection.find()
    for player in players:
        result.add(player["name"])
    return result

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

