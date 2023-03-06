from collections import OrderedDict
from entities.rules import Rule


class ScoreCard:
    def __init__(self, rules: list[Rule]) -> None:
        self._score_map = OrderedDict()
        self._marked_map = {}
        for rule in rules:
            self._score_map[rule.name] = 0
            self._marked_map[rule.name] = False

    def mark_rule(self, rule_name: str, score: int):
        if self.is_marked(rule_name):
            raise ValueError("This rule has been filled")
        self._score_map[rule_name] = score
        self._marked_map[rule_name] = True

    def is_marked(self, rule_name):
        return self._marked_map[rule_name]

    def get_total(self):
        return sum(filter(lambda v: v, self._score_map.values()))
    
    def get_scoremap(self):
        return self._score_map
    
    def get_score_for_rule(self, rule_name):
        return self._score_map[rule_name]

            