from collections import OrderedDict
from rules import Rule


class ScoreCard:
    def __init__(self, rules: list[Rule]) -> None:
        self._score_map = OrderedDict()
        for rule in rules:
            self._score_map[rule.id] = 0

    def mark_rule(self, rule_id: str, score: int):
        if self._score_map[rule_id]:
            raise ValueError("This rule has been filled")
        self._score_map[rule_id] = score

    def get_total(self):
        return sum(self._score_map.values())
    
    def get_scoremap(self):
        return self._score_map




