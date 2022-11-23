import os
from datetime import datetime
from .player import Player, Team
from .fifaBot import game_input, team_game_input, display_player, output_twoleaderboard
from .fifaBot import display_head_to_head, output_leaderboard, chance, chance_teams
from .fifaBot import probability_to_moneyline, display_team, display_twos_head_to_head
from .database_interactions import download_player, get_player_names, get_team_keys, get_hashable_key
from .database_interactions import add_player, add_team, download_team

helpMessage = '''**Commands:**

**LEADERBOARD**
*“!leaderboard”*
See the leaderboard of the best and worst members of Sigma United.
*“!twoleaderboard”*
See the leaderboard of the best and worst duos in Sigma United.

**ADD GAME**
Singles game: *"!game (winner name) (loser name) (winner goals)-(loser goals)”*
Doubles game: *"!twogame (winner #1 name) (winner #2 name)) (loser #1 name) (loser #2 name) (winner goals)-(loser goals)”* 
Add a new game. Input winner and loser names, and goals scored.  

**STATS** 
*“!stats (player 1) (optional player2)”* 
Check your stats. Add two names for head to head, and one name for your record. 
*“!teamstats (player 1) (player2) (optional player3 player4)”* 
Check your stats as a duo. Add two duos for head to head.

**NEW PLAYER** 
*“!newplayer (name)”* 
Add a new player to the fifa rankings. 
*“!newteam (player1) (player2)”* 
Add a new duo to the doubles rankings.

**(NEVER) TELL ME THE ODDS** 
*“!chance (player1) (player2)”* 
Get the odds of either player winning and the associated moneylines.
*“!chance (player1) (player2) (player3) (player4)”*
Get the odds of either duo winning and the associated moneylines. 

**HELP** 
*“!fifahelp”* 
This is your help!'''

def bang_game(text: list[str]) -> str:
    valid_players = get_player_names()
    if len(text) != 4:
        return 'Error in formatting the message: should be of the format "!game (winner name) (loser name) (score-score)"'
    elif text[1] not in valid_players or text[2] not in valid_players:
        return 'Missing player: one or both of the player names are not in the database. Initialize the new player or check spelling.'
    scores = text[3].split("-")
    if int(scores[0]) < int(scores[1]):
        return "Change your names and scores around: winner should come first!"
    else:
        game_input(datetime.now(), text[1], text[2], int(scores[0]), int(scores[1]))
        return f'{text[2]} got shit on!'

def bang_twogame(text: list[str]) -> str:
    valid_players = get_player_names()
    valid_teams = get_team_keys()
    if len(text) != 6:
        return 'Error in formatting the message: should be of the format "!game (winner1 name) (winner2 name) (loser1 name) (loser2 name) (score-score)"'
    elif text[1] not in valid_players or text[2] not in valid_players or text[3] not in valid_players or text[4] not in valid_players:
        return 'Missing player: one or multiple player names are not in the database. Initialize the new player or check spelling.'
    winner_key = get_hashable_key(text[1], text[2])
    loser_key = get_hashable_key(text[3], text[4])
    if (loser_key not in valid_teams):
        return "losing team not recognized. initialize with !newteam"
    elif (winner_key not in valid_teams):
        return "winning team not recognized. initialize with !newteam"
    scores = text[5].split("-")
    if int(scores[0]) < int(scores[1]):
        return "Change your names and scores around: winner should come first!"
    else:
        team_game_input(datetime.now(), text[1], text[2], text[3], text[4], scores[0], scores[1]) #FIX
        return f'lmao {text[3]} and {text[4]} are trash'

def bang_stats(text: list[str]) ->str:
    valid_players = get_player_names()
    if (len(text) == 2):
        #one player case
        if text[1] not in valid_players:
            return "player not found"
        else:
            return display_player(text[1])
    elif (len(text) == 3):
        if text[1] not in valid_players:
            return "first player not found"
        elif text[2] == "SP":
            return display_player(text[1], "SP")
        elif text[2] == "MP":
            return display_player(text[1], "MP")
        elif text[2] not in valid_players:
            return  "second player not found"
        else:
            return display_head_to_head(text[1], text[2])
    else:
        return 'Error in formatting the message: should be of the format "!stats (playername) optional(playername)"'

def bang_teamstats(text: list[str]) -> str:
    valid_teams = get_team_keys()
    if (len(text) not in [3, 5]):
        return 'Error in formatting the message: should be of the format "!stats (playername) (playername) optional(playername playername)"'
    if (len(text) == 3):
        #single team stats
        key = get_hashable_key(text[1], text[2])
        if (key not in valid_teams):
            return "Team not initialized. try !newteam"
        else:
            team = download_team(text[1], text[2])
            return display_team(team)
    #double team head-to-head
    key1 = get_hashable_key(text[1], text[2])
    key2 = get_hashable_key(text[3], text[4])
    if (key1 not in valid_teams):
        return "first team not initialized. try !newteam"
    elif (key2 not in valid_teams):
        return  "second team not initalized. try !newteam"
    team1 = download_team(text[1], text[2])
    team2 = download_team(text[3], text[4])
    return display_twos_head_to_head(team1, team2)
    
def bang_leaderboard() -> str:
    return output_leaderboard()

def bang_twoleaderboard() -> str:
    return output_twoleaderboard()

def bang_fifahelp() -> str:
    return helpMessage

def bang_newplayer(text: list[str]) -> str:
    valid_players = get_player_names()
    if len(text) != 2:
        return 'Error in formatting the message: should be of the format "!newplayer (playername)"'
    elif text[1] not in valid_players: 
        command, output = text
        add_player(output)
        return 'Added! '+output
    return "player already in database"

def bang_newteam(text: list[str]) -> str:
    valid_teams = get_team_keys()
    valid_players = get_player_names()
    if (len(text) != 3):
        return 'Error in formatting the message: should be of the format "!newplayer (player1) (player2)"'
    else:
        player1 = text[1]
        player2 = text[2]
        if (player1 not in valid_players):
            return "First player not recognized. Initialize them first with !newplayer"
        elif (player2 not in valid_players):
            return "Second player not recognized. Initialize them first with !newplayer"
        key = get_hashable_key(player1, player2)
        if (key not in valid_teams):
            add_team(player1, player2)
            return "Added! " + player1 + ", " + player2
        return "Team already initialized"

def bang_chance(text: list[str]) -> str:
    valid_players = get_player_names()
    valid_teams = get_team_keys()
    if (len(text) not in [3,5]):
        return 'Error in formatting the message, should be of the format !chance (lpayer1name) (player2name)'
    if (len(text) == 3):
        player1: Player = download_player(text[1])
        player2: Player = download_player(text[2])
        if (player1.name not in valid_players):
            return "first player not recognized"
        elif (player2.name not in valid_players):
            return "second player not recognized"
        p, q = chance(player1, player2)
        p_ml, q_ml = probability_to_moneyline(p), probability_to_moneyline(q)
        output = f'{"Names" : ^15}|{"P(win)": ^10}|{"ML": ^10}\n'
        output += "-" * 15 + "|" + "-"*10 + "|" + "-" * 10 + "\n"
        output += f'{player1.name : <15}{round((p*100),1): >9}%|{"+" + str(p_ml) if p_ml > 0 else str(p_ml): >10}\n'
        output += f'{player2.name : <15}{round((q*100),1): >9}%|{"+" + str(q_ml) if q_ml > 0 else str(q_ml): >10}'
        return output

    team1key = get_hashable_key(text[1], text[2])
    team2key = get_hashable_key(text[3], text[4])
    if (team1key not in valid_teams):
        return "first team not recognized. try initializing with !newteam"
    elif (team2key not in valid_teams):
        return "second team not recognized. try initializing with !newteam"
    team1: Team = download_team(text[1], text[2])
    team2: Team = download_team(text[3], text[4])
    p,q  = chance_teams(team1, team2)
    p_ml, q_ml = probability_to_moneyline(p), probability_to_moneyline(q)
    output = f'{"Names" : ^15}|{"P(win)": ^10}|{"ML": ^10}\n'
    output += "-" * 15 + "|" + "-"*10 + "|" + "-" * 10 + "\n"
    output += f'{team1.player1 + "-" + team1.player2 : <15}{round((p*100),1): >9}%|{"+" + str(p_ml) if p_ml > 0 else str(p_ml): >10}\n'
    output += f'{team2.player1 + "-" + team2.player2 : <15}{round((q*100),1): >9}%|{"+" + str(q_ml) if q_ml > 0 else str(q_ml): >10}'
    return output