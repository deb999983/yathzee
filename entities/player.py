from entities.score_card import ScoreCard


class Player:
    def __init__(self, name:str, score_card: ScoreCard) -> None:
        self.name = name
        self.score_card = score_card
        self.current_dices = []
        self.dices_to_roll = []
    
    def score(self):
        return self.score_card.get_total()

    def roll(self):
        pass

    def choose_result(self, rule_id):
        self.score_card.mark_rule(rule_id)
