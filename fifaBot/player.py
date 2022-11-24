class Player:
    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of Player.")
        return super().__new__(cls)

    def __init__(self, name, elo, wins, losses, games_played, goals_for, goals_against, goal_differential, two_wins, two_losses, two_games_played):
        print("2. Initialize the new instance of Player.")
        self.name = name
        self.elo = elo
        self.wins = wins
        self.losses = losses
        self.games_played = games_played
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.goal_differential = goal_differential
        self.two_wins = two_wins
        self.two_losses = two_losses
        self.two_games_played = two_games_played
        
    def get_record(self) -> list[int]:
        return [self.wins, self.losses]

    def get_goals_per_game(self) -> int:
        return self.goals_for/self.games_played

    def get_goals_against_per_game(self) -> int:
        return self.goals_against/self.games_played

    def get_solo_win_percentage(self) -> float:
        if self.games_played == 0:
            return 0.00
        return round(self.wins/self.games_played*100, 2)

    def get_one_player_stats(self) -> str:
        if self.games_played == 0:
            return f"No singleplayer stats available. 0 singleplayer games played"
        return f" Singleplayer: {self.name} ({self.elo})\
            \n Win %: {self.get_solo_win_percentage()}  W-L: {self.wins}-{self.losses}  MP: {self.games_played}\
            \n GD: {self.goal_differential}  GF/Game: {round(self.get_goals_per_game(), 2)}  GA/Game: {round(self.get_goals_against_per_game(), 2)} "

    def get_two_player_stats(self) -> str:
        if self.two_games_played == 0:
            return f"No multiplayer stats available. 0 multiplayer games played"
        return  f" Multiplayer: {self.name} \n W-L: {self.two_wins}-{self.two_losses}  MP: {self.two_games_played} "

    def __repr__(self) -> str:
        if self.games_played == 0 or self.two_games_played == 0:
            return f"Full stats not available. Choose \"SP\" or \"MP\" stats"
        return f" {type(self).__name__} {self.name} ({self.elo}) \n W-L: {self.wins}-{self.losses}  MP: {self.games_played} GD: {self.goal_differential}\
            \n GF/Game: {round(self.get_goals_per_game(), 2)}  GA/Game: {round(self.get_goals_against_per_game(), 2)}\
            \n Doubles W-L: {self.two_wins}-{self.two_losses}  Doubles MP: {self.two_games_played}"


class Team: 
    def __init__(self, player1: str, player2: str, elo:int, wins:int, losses: int, 
        key: str, games_played: int) -> None:
        self.player1 = player1
        self.player2 = player2
        self.key = key
        self.elo = elo
        self.wins = wins
        self.losses =losses
        self.games_played = games_played
    
    def get_record(self) -> list[int]:
        return [self.wins, self.losses]
    
    def __repr__(self) -> str:
        return f"{self.key} ({self.elo})  W-L: {self.wins}-{self.losses}  MP: {self.games_played}"
