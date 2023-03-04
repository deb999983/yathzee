import random


class Dice:
    def __init__(self, id) -> None:
        self.id = id
        self.current_value = None
    
    def roll(self) -> int:
        self.current_value = random.randint(1, 6)
        return self.current_value

    def display(self):
        pass
