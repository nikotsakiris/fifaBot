import discord
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from .player import Player, Team
from .game import Game
from .database_interactions import download_player, download_players, add_player, get_player_names, add_game
from .database_interactions import update_head_to_head, get_hashable_key, get_database, update_player_in_mongo
from .database_interactions import add_twogame, download_team, update_team_in_mongo, get_team_keys
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
        return_string += str(player.name) + ": " + str(player.elo) + " record: "+str(player.wins)+" - "
        return_string += str(player.losses)+", gp: "+str(player.games_played)+", gd: "+str(player.goal_differential)+" \n"
    return return_string


def output_twoleaderboard():
    db = get_database()
    collection = db["Teams"]
    teams = collection.find()
    elo_tuples: list[tuple[any, int]] = []

    for team in teams:
        elo_tuples.append((team, int(team["elo"])))
    
    sorted_elo_tuples = sorted(elo_tuples, key = lambda t: t[1], reverse=True) #sort teams based on elo

    return_string = "Current Doubles Leaderboard: \n"
    for elo_tuple in sorted_elo_tuples:
        team = elo_tuple[0]
        return_string += str(team["key"]+ ": " + str(team["elo"]) + " record : " + str(team["wins"]) + " - ")
        return_string += str(team["losses"]) + '\n'

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
    goal_differential = game.winner_score - game.loser_score
    player1.goal_differential += goal_differential
    player2.goal_differential -= goal_differential

    if player_1_won: 
        player1.wins += 1
        player2.losses += 1
        player1.goals_for += game.winner_score
        player2.goals_against += game.winner_score
        player1.goals_against += game.loser_score
        player2.goals_for += game.loser_score
    else:
        player2.wins += 1
        player1.losses += 1
        player2.goals_for += game.winner_score
        player1.goals_against += game.winner_score
        player2.goals_against += game.loser_score
        player1.goals_for += game.loser_score
    
    player1.games_played += 1
    player2.games_played += 1


def probability_to_moneyline(prob):
    if prob >= 0.5:
        return int(-(prob)/(1 - prob) * 100)
    else:
        return int((1-prob)/prob * 100)
    
def chance(player1: Player, player2: Player) -> tuple[float]:
    #should return a list 2 of two numbers, where:
        #result[0] = player1's chance of winning
        #result[1] = player2's chance of winning

    p = calc_expected_wins(player1.elo, player2.elo)
    return (p, 1-p,)


        

def chance_teams(team1: Team, team2: Team) -> tuple[float]:
    p = calc_expected_wins(team1.elo, team2.elo)
    return (p, 1-p)



 



def get_hashable_key(winner: str, loser: str) -> str:
    key_list = [winner, loser]
    key_list.sort()
    return key_list[0] + "-" + key_list[1]




def display_head_to_head(player1: str, player2 : str) -> str:
    key = get_hashable_key(player1,player2)
    db = get_database()
    collection = db["HeadToHead"]
    item = collection.find_one( {"key" : key })
    if (not item):
        return "These two players don't seem to have a head to head record."
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

    

def team_game_input(date, winner1, winner2, loser1, loser2, winner_score, loser_score):

    # add_game(winner1+winner2, loser1+loser2, [winner_score, loser_score], date)
    
    # players = [download_player(winner1), download_player(winner2), download_player(loser1), download_player(loser2)]
    # update_2player_info(players[0],players[1],players[2],players[3])
    
    # for i in range(4):
    #     update_player_in_mongo(players[i])


    add_twogame(winner1, winner2, loser1, loser2, date, [winner_score, loser_score])
    winning_team = download_team(winner1, winner2)
    losing_team = download_team(loser1, loser2)
    update_2player_info(winning_team, losing_team)
    update_team_in_mongo(winning_team)
    update_team_in_mongo(losing_team)
    



def update_2player_info(winning_team: Team, losing_team: Team) -> None:
    # team1_elo = (winner1.elo + winner2.elo)/2
    # team2_elo = (loser1.elo + loser2.elo)/2
    
    # elo_deltas = calculate_elo_changes(team1_elo,team2_elo,True)

    # winner1.elo += int(elo_deltas[0]/2)
    # winner2.elo += int(elo_deltas[0]/2)
    # loser1.elo += int(elo_deltas[1]/2)
    # loser2.elo += int(elo_deltas[1]/2)

    winning_elo = winning_team.elo
    losing_elo = losing_team.elo
    elo_deltas = calculate_elo_changes(winning_elo, losing_elo, True)
    winning_team.elo += int(elo_deltas[0])
    losing_team.elo += int(elo_deltas[1])
    
    winning_team.games_played += 1
    losing_team.games_played += 1
    winning_team.wins += 1
    losing_team.losses += 1
    



def display_player(player_name : str):
    player_obj = download_player(player_name)
    return repr(player_obj)



