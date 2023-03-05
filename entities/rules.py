from collections import Counter


class Rule:
    def __init__(self, **kwargs) -> None:    
        self.id = kwargs["id"]
        self.name = kwargs["name"]
    def get_score(self, dices: list[int]) -> int:
        pass


class CountOnlyOne(Rule):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "only_ones"), name=kwargs.get("name", "Only Ones"))
        
    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 1, dices))


class CountOnlyTwo(Rule):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "only_twos"), name=kwargs.get("name", "Only Twos"))

    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 2, dices))


class CountOnlyThree(Rule):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "only_threes"), name=kwargs.get("name", "Only Threes"))

    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 3, dices))


class CountOnlyFour(Rule):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "only_fours"), name=kwargs.get("name", "Only Fours"))

    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 4, dices))


class CountOnlyFive(Rule):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "only_fives"), name=kwargs.get("name", "Only Fives"))

    def get_score(self, dices: list[int]) -> int:
        return sum(filter(lambda d: d == 5, dices))


class CountOnlySix(Rule):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "only_sixes"), name=kwargs.get("name", "Only Sixes"))

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
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "three_of_a_kind"), name=kwargs.get("name", "Three of a Kind"))

    def get_score(self, dices: list[int]) -> int:
        if not self.is_kind(3, dices):
            return 0
        return sum(dices)


class FourOfAKind(Rule, OfAKindMixin):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "four_of_a_kind"), name=kwargs.get("name", "Four of a Kind"))

    def get_score(self, dices: list[int]) -> int:
        if not self.is_kind(4, dices):
            return 0
        return 36


class FiveOfAKind(Rule):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "five_of_a_kind"), name=kwargs.get("name", "Five of a Kind"))

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
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "four_in_a_row"), name=kwargs.get("name", "Four in a row"))

    def get_score(self, dices: list[int]) -> int:
        if not self.in_a_row(4, dices):
            return 0
        return 36


class FiveInARow(Rule, InARowMixin):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "five_in_a_row"), name=kwargs.get("name", "Five in a Row"))

    def get_score(self, dices: list[int]) -> int:
        if not self.in_a_row(4, dices):
            return 0
        return 50


class Anything(Rule):
    def __init__(self, **kwargs) -> None:
        super().__init__(id=kwargs.get("id", "anything"), name=kwargs.get("name", "Anything"))
    
    def get_score(self, dices: list[int]) -> int:
        return sum(dices)



