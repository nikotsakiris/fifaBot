from datetime import datetime

class Game:
    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of Game.")
        return super().__new__(cls)

    def __init__(self, date, winner, loser, winner_score, loser_score):
        print("2. Initialize the new instance of Game.")
        self.date = date # date 'MM/DD/YYYY'
        self.winner = winner #'player_name'
        self.loser = loser #'player_name'
        self.winner_score = winner_score
        self.loser_score = loser_score

    def __repr__(self) -> str:
        return f"{type(self).__name__}(date={self.date}, winner={self.winner}, loser={self.loser})"

class TwoGame:
    def __init__(self, winner1: str, winner2: str, key: str, 
        loser1: str, loser2 : str, date: datetime, winner_score : int, loser_score: int ) -> None:

        self.date = date
        self.winner1 = winner1
        self.winner2 = winner2
        self.loser1 = loser1
        self.loser2 = loser2
        self.winner_score = winner_score
        self.loser_score = loser_score
        self.key = key
        
    