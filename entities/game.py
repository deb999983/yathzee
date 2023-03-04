from entities.player import Player
from entities.rules import Rule
from entities.score_card import ScoreCard


class Game:
    def __init__(self) -> None:
        self._rules: list(Rule) = []
        self.players = []
    
    def add_rule(self, rule: Rule):
        self._rules.append(rule)
        return self

    def add_player(self, player_name):
        score_card = ScoreCard(self._rules)
        player = Player(player_name, score_card)
        self.players.append(player)
