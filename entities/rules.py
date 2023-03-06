from collections import Counter


class Rule:
    def get_score(self, dices: list[int]) -> int:
        pass


class CountOnlyOne(Rule):
    name = "Only Ones"
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 1, dices))


class CountOnlyTwo(Rule):
    name = "Only Twos"
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 2, dices))


class CountOnlyThree(Rule):
    name = "Only Threes"
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 3, dices))


class CountOnlyFour(Rule):
    name = "Only Fours"
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 4, dices))


class CountOnlyFive(Rule):
    name = "Only Fives"
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 5, dices))


class CountOnlySix(Rule):
    name = "Only Sixes"
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 6, dices))


class OfAKindMixin:
    def is_kind(self, count: int, dices: list[int]) -> bool:
        f_map = Counter(dices)
        for _, c in f_map.items():
            if c == count:
                return True
        return False


class ThreeOfAKind(Rule, OfAKindMixin):
    name = "Three of a Kind"
    def get_score(self, dices: list[int]) -> int:
        if not self.is_kind(3, dices):
            return 0
        return sum(dices)


class FourOfAKind(Rule, OfAKindMixin):
    name = 'Four of a Kind'
    def get_score(self, dices: list[int]) -> int:
        if not self.is_kind(4, dices):
            return 0
        return 36


class FiveOfAKind(Rule):
    name = "Five of a Kind"
    def get_score(self, dices: list[int]) -> int:
        if not self.is_kind(5, dices):
            return 0
        return 50
    

class InARowMixin:
    def in_a_row(self, count: int, dices: list[int]) -> bool:
        dices = sorted(set(dices))
        i, L = 0, len(dices)
        c = 1
        while i < L - 1:
            if dices[i + 1] != dices[i] + 1:
                c = 1
            else:
                c = c + 1
                if c == count:
                    return True
            i = i + 1
        return False


class FourInARow(Rule, InARowMixin):
    name = "Four in a row"
    def get_score(self, dices: list[int]) -> int:
        if not self.in_a_row(4, dices):
            return 0
        return 36


class FiveInARow(Rule, InARowMixin):
    name = "Five in a Row"
    def get_score(self, dices: list[int]) -> int:
        if not self.in_a_row(4, dices):
            return 0
        return 50


class Anything(Rule):
    name = "Anything"
    def get_score(self, dices: list[int]) -> int:
        return sum(dices)


YATHZEE_RULES = [FourOfAKind(), FourInARow()]
