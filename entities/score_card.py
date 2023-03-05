from collections import OrderedDict
from rules import Rule


class ScoreCard:
    def __init__(self, rules: list[Rule]) -> None:
        self._score_map = OrderedDict()
        self.marked_map = {}
        for rule in rules:
            self._score_map[rule.name] = 0
            self.marked_map[rule.name] = False

    def mark_rule(self, rule_name: str, score: int):
        if self.marked_map[rule_name]:
            raise ValueError("This rule has been filled")
        self._score_map[rule_name] = score
        self.marked_map[rule_name] = True

    def get_total(self):
        return sum(filter(lambda v: v, self._score_map.values()))
    
    def get_scoremap(self):
        return self._score_map
            