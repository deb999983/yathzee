from entities.rules import Rule
from entities.score_card import ScoreCard


class Player:
    def __init__(self, name:str, score_card: ScoreCard) -> None:
        self.name = name
        self.score_card = score_card
        self.saved_dices = []
        self.dices_to_roll = 4
    
    def score(self):
        return self.score_card.get_total()

    def roll(self):
        pass

    def choose_result(self, rule_id):
        self.score_card.mark_rule(rule_id)

    @classmethod
    def generate_possible_scores(cls, rules: list[Rule], dices: list[int]):        
        card = ScoreCard(rules)
        for rule in rules:
            card.mark_rule(rule.name, rule.get_score(dices))
        return card
