from functools import cached_property

from display.table import DisplayComponent, Table
from entities.score_card import ScoreCard


class ScoreCardDisplay(DisplayComponent):
    def __init__(self, score_card=ScoreCard, title='', display_total=True) -> None:
        self.score_card = score_card.get_scoremap()
        self.name = title
        self.display_total = display_total

        score_data = self.prepare_score_data(score_card)
        self.score_table = Table(
            headers=["S-No", "Title", "Score"],
            data=score_data,
            name=title
        )


    def prepare_score_data(self, score_card) -> list[tuple]:
        score_data = [(str(index + 1), rule_score[0], str(rule_score[1]) if rule_score[1] or score_card.is_marked(rule_score[0]) else '') for index, rule_score in enumerate(self.score_card.items())]

        if self.display_total:
            score_data.append(
                (str(len(score_data) + 1), 'Total', str(score_card.get_total()),)
            )
        return score_data

    @cached_property
    def data(self):
        return self.score_table.data
