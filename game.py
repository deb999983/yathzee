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
        self.players = [
            Player(name="John", score_card=ScoreCard(self._rules)),
            Player(name="Bob", score_card=ScoreCard(self._rules))
        ]
        self.round = 0
        self.width = 100
    
    def add_rule(self, rule: Rule):
        self._rules.append(rule)
        return self

    def add_player(self, player_name):
        score_card = ScoreCard(self._rules)
        player = Player(player_name, score_card)
        self.players.append(player)

    def over(self) -> bool:
        return self.round == 8

    def next_round(self):
        print(f"Round {self.round} Starts".center(self.width, "+") + "\n")
        for player in self.players:
            player.next_turn(self._rules)
        print(f"Round {self.round} Ends".center(self.width, "+") + "\n")   

    def pick_winner(self) -> Player:
        winner: Player = None
        max_score: int = 0 
        for player in self.players:
            total_score = player.score()
            if total_score >= max_score:
                winner = player
                max_score = total_score
        return winner

    def start(self):
        while not self.over():
            self.next_round()
            self.round = self.round + 1
        
        # Display score cards
        Display(
            *[ScoreCardDisplay(player.score_card, title=f"{player.name} Scorecard") for player in self.players]
        )
        
        # Pick Winner
        winner = self.pick_winner()
        print(f"  Winner is {winner.name}, with a score of {winner.score()}  ".center(self.width, '*') + "\n")


def run():
    g = Game()
    g.start()

run()