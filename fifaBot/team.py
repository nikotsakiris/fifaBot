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
