from display.score_card import ScoreCardDisplay
from display.table import Display
from entities.player import Player
from entities.rules import Rule, CountOnlyOne, CountOnlyTwo, CountOnlyThree, CountOnlyFour, ThreeOfAKind, FourOfAKind, FourInARow, Anything
from entities.score_card import ScoreCard


class Game:
    def __init__(self) -> None:
        self._rules: list(Rule) = [
            CountOnlyOne(),
            CountOnlyTwo(),
            CountOnlyThree(),
            CountOnlyFour(),
            ThreeOfAKind(),
            FourOfAKind(),
            FourInARow(),
            Anything(),
        ]
        self.players = []
        self.round = 0
        self.width = 100
        self.max_dices = 4
    
    def add_player(self, player_name):
        score_card = ScoreCard(self._rules)
        player = Player(player_name, score_card)
        self.players.append(player)

    def over(self) -> bool:
        return self.round == len(self._rules)

    def next_round(self):
        print(f"Round {self.round} Starts".center(self.width, "+") + "\n")
        for player in self.players:
            player.next_turn(self.max_dices, self._rules)
        print(f"Round {self.round} Ends".center(self.width, "+") + "\n")   

    def show_winner(self) -> Player:
        # Display the score card.
        Display(
            *[ScoreCardDisplay(player.score_card, title=f"{player.name} Scorecard") for player in self.players]
        )

        # Select Winner
        winner: Player = None
        max_score: int = 0 
        for player in self.players:
            total_score = player.score()
            if total_score >= max_score:
                winner = player
                max_score = total_score
        
        # Show Winner
        print(f"  Winner is {winner.name}, with a score of {winner.score()}  ".center(self.width, '*') + "\n")

    def add_players(self):
        choice = 'y'
        while choice in ['y', 'Y', 'YES', 'yes']:
            player_name = input("Enter player name: ")
            self.add_player(player_name)            
            choice = input("Add new player (y/n)?")

    def start(self):
        self.add_players()
        while not self.over():
            self.round = self.round + 1
            self.next_round()
        
        # Display score cards and Pick Winner
        self.show_winner()

def run():
    g = Game()
    g.start()

run()