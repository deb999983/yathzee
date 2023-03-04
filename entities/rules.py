from collections import Counter


class Rule:
    def __init__(self, id, name, desc) -> None:
        self.id = id
        self.name = name
        self.desc = desc
    
    def get_score(self, dices: list[int]) -> int:
        pass


class CountOnlyOne(Rule):
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 1, dices))


class CountOnlyTwo(Rule):
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 2, dices))


class CountOnlyThree(Rule):
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 3, dices))


class CountOnlyFour(Rule):
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 4, dices))


class CountOnlyFive(Rule):
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 5, dices))


class CountOnlySix(Rule):
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
    def get_score(self, dices: list[int]) -> int:
        if not self.is_kind(3, dices):
            return 0
        return sum(dices)


class FourOfAKind(Rule, OfAKindMixin):
    def get_score(self, dices: list[int]) -> int:
        if not self.is_kind(4, dices):
            return 0
        return 36


class FiveOfAKind(Rule):
    def get_score(self, dices: list[int]) -> int:
        if not self.is_kind(5, dices):
            return 0
        return 50
    

class InARowMixin:
    def in_a_row(self, count: int, dices: list[int]) -> bool:
        dices = sorted(dices)
        i, L = 0, len(dices)
        while i < L:
            j, c = i + 1, 1
            while j < L:
                if dices[j] != dices[j - 1] + 1:
                    break
                c = c + 1
                j = j + 1            
            if c == count:
                return True
            i = j
        return False


class FourInARow(Rule, InARowMixin):
    def get_score(self, dices: list[int]) -> int:
        if not self.in_a_row(4, dices):
            return 0
        return 36


class FiveInARow(Rule, InARowMixin):
    def get_score(self, dices: list[int]) -> int:
        if not self.in_a_row(4, dices):
            return 0
        return 50


class Anything(Rule):
    def get_score(self, dices: list[int]) -> int:
        return 50


