import random
import time
from display.dice import Dice
from display.score_card import ScoreCardDisplay
from display.table import Display
from entities.rules import Rule
from entities.score_card import ScoreCard


class Player:
    def __init__(self, name:str, score_card: ScoreCard) -> None:
        self.name = name
        self.score_card = score_card
        self.saved_dices = []
        self.dices_to_roll = 4
        self.width = 100
    
    def score(self):
        return self.score_card.get_total()

    def choose_result(self, rule_id):
        self.score_card.mark_rule(rule_id)

    @classmethod
    def generate_possible_scores(cls, rules: list[Rule], dices: list[int]):        
        card = ScoreCard(rules)
        for rule in rules:
            card.mark_rule(rule.name, rule.get_score(dices))
        return card

    def next_turn(self, game_rules: list[Rule]):
        player = self
        print(f"{player.name} Turn".center(self.width, "-") + "\n")
        player.saved_dices = []
        player.dices_to_roll = 4
        for i in range(3):
            rolled_dices = self.roll_dices()
            if rolled_dices:
                display_dices = []
                if player.saved_dices:
                    display_dices.append(Dice(player.saved_dices, name=f"Turn {i + 1}, Saved Dices..."))
                display_dices.append(Dice(rolled_dices, name=f"Turn {i + 1}, Rolled {player.dices_to_roll} Dices..."))
                Display(*display_dices)

            all_dices = [*player.saved_dices, *rolled_dices] 
            Display(
                ScoreCardDisplay(self.score_card, title="Your Score"),
                Dice(all_dices, name=f"Turn {i + 1}, Current Combination:", include_id_header=True),
                ScoreCardDisplay(Player.generate_possible_scores(game_rules, all_dices), title="Possible Scores With This Combination.")
            )

            if rolled_dices and i + 1 < 3:
                choice = input("Select score and end turn(y/n)? ")
                if choice == "y":
                    self.mark_rule(game_rules, all_dices)
                    break
                else:
                    dices_to_keep = input("Select dices to keep (comma separated ids. Ex: 2,1,3): ")
                    if dices_to_keep:
                        dices_to_keep = list(map(int, dices_to_keep.split(',')))
                        player.saved_dices = [all_dices[index - 1] for index in dices_to_keep]
                        player.dices_to_roll = 4 - len(player.saved_dices)
                    else:
                        player.saved_dices = []
                        player.dices_to_roll = 4
            else:
                self.mark_rule(game_rules, all_dices)

        print(f"End {player.name} Turn".center(self.width, "-") + "\n")
        return
    
    def roll_dices(self):
        if not self.dices_to_roll:
            return []
        return [random.randint(1, 6) for i in range(self.dices_to_roll)]

    def choose_score(self, game_rules: list[Rule], all_dices: list[int]):
        choice = None
        while not choice:
            try:
                choice = int(input("Choose a serial no from possible scores: "))
                game_rules[choice - 1] # Test index
            except Exception:
                print(f"Invalid Score choosen, please pick a valid score.".center(self.width, "."))
                choice = None
        return choice - 1
    
    def mark_rule(self, game_rules, all_dices:list[int]):
        while True:
            rule = None
            try:
                score_choice = self.choose_score(game_rules, all_dices)
                rule = game_rules[score_choice]
                self.score_card.mark_rule(rule.name, rule.get_score(all_dices))
                break
            except ValueError as e:
                print("\n")
                print(f"You have already selected [{rule.name}], please select a different score".center(self.width, '.'))
