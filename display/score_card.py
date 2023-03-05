from functools import cached_property

from display.table import Table
from entities.score_card import ScoreCard


class ScoreCardDisplay:
    def __init__(self, score_card=ScoreCard, title='') -> None:
        self.score_card = score_card.get_scoremap()
        score_data = [(str(index + 1), rule_score[0], str(rule_score[1]) if rule_score[1] or score_card.marked_map[rule_score[0]] else '') for index, rule_score in enumerate(self.score_card.items())]
        score_data.append(
            (str(len(score_data) + 1), 'Total', str(score_card.get_total()),)
        )
        self.score_table = Table(
            headers=["S-No", "Title", "Score"],
            data=score_data,
            name=title
        )
        self.name = title
        
    @cached_property
    def data(self):
        return self.score_table.data
