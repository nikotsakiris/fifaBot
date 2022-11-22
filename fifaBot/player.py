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
        return f"{self.name} {self.elo}, record: {self.wins} - {self.losses}, gp: {self.games_played}"



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
