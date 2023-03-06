import random
import time
from display.dice import Dice
from display.score_card import ScoreCardDisplay
from display.table import Display
from entities.rules import YATHZEE_RULES, Rule
from entities.score_card import ScoreCard


class Player:
    def __init__(self, name:str, score_card: ScoreCard) -> None:
        self.name = name
        self.score_card = score_card
        self.saved_dices = []
        self.width = 100
        self.max_dices = 4
    
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

    def yahtzee_formed(self, possible_scores: ScoreCard) -> Rule:
        possible_yathzees = list(filter(lambda r: possible_scores.get_score_for_rule(r.name), YATHZEE_RULES))
        possible_yathzees = list(filter(lambda r: not self.score_card.is_marked(r.name), possible_yathzees))
        return possible_yathzees and possible_yathzees[0]

    def next_turn(self, max_dices: int, game_rules: list[Rule]):
        player = self
        print(f"{player.name} Turn".center(self.width, "-") + "\n")
        player.saved_dices = []
        dices_to_roll = max_dices
        for i in range(3):            
            rolled_dices = self.roll_dices(dices_to_roll, i)
            all_dices = [*player.saved_dices, *rolled_dices] 

            possible_scores = Player.generate_possible_scores(game_rules, all_dices)

            # End turn if yathzee.
            yahtzee_formed = self.yahtzee_formed(possible_scores)
            if yahtzee_formed:
                self.score_card.mark_rule(yahtzee_formed.name, yahtzee_formed.get_score(all_dices))
                Display(
                    ScoreCardDisplay(self.score_card, title=" Yathzeeeeeeee .... "),
                    Dice(all_dices, name=f"Yathzee Combination: [-- {yahtzee_formed.name} --]", include_id_header=True),
                )
                input(f"[-- {yahtzee_formed.name} --] was automatically marked, press any key to continue:")
                break
                    

            rolled_dices and Display(
                ScoreCardDisplay(self.score_card, title="Your Score"),
                Dice(all_dices, name=f"Turn {i + 1}, Current Combination:", include_id_header=True),
                ScoreCardDisplay(possible_scores, title="Possible Scores With This Combination.", display_total=False)
            )
            # Last turn, or all dices saved in the last round that means no new dices rolled, mark rule.
            if not rolled_dices or i == 2:
                self.mark_rule(game_rules, all_dices)
                break
            
            # Or select dices to save, remaining no of dices in the next turn.
            choice = input("Select score and end turn(y/n)? ")
            if choice == "y":
                self.mark_rule(game_rules, all_dices)
                break
            else:
                dices_to_roll = self.select_dices(all_dices)

        print(f"End {player.name} Turn".center(self.width, "-") + "\n")
    
    def roll_dices(self, dices_to_roll, turn_no):
        rolled_dices = [] if not dices_to_roll else [random.randint(1, 6) for i in range(dices_to_roll)]
        if not rolled_dices:
            return []
        if not self.saved_dices:
            Display(
                Dice(rolled_dices, name=f"Turn {turn_no + 1}, Rolled {dices_to_roll} Dices...")
            )
        else:
            Display(
                Dice(self.saved_dices, name=f"Turn {turn_no + 1}, Saved Dices..."),
                Dice(rolled_dices, name=f"Turn {turn_no + 1}, Rolled {dices_to_roll} Dices...")
            )
        return rolled_dices

    def choose_score(self, game_rules: list[Rule]):
        choice = None
        while not choice:
            try:
                choice = int(input("Choose a serial no from possible scores: "))
                game_rules[choice - 1] # Test index
            except Exception:
                print(f"  Invalid Score choosen, please pick a valid score.  ".center(self.width, "x"))
                choice = None
        return choice - 1
    
    def mark_rule(self, game_rules, all_dices:list[int]):
        while True:
            rule = None
            try:
                score_choice = self.choose_score(game_rules)
                rule = game_rules[score_choice]
                self.score_card.mark_rule(rule.name, rule.get_score(all_dices))
                break
            except ValueError as e:
                print("\n")
                print(f"  You have already selected [{rule.name}], please select a different score  ".center(self.width, 'x'))

    def select_dices(self, all_dices:list[int]):
        dices_to_keep, dices_to_roll = None, 0
        while dices_to_keep is None:
            dices_to_keep = input("Select dices to keep (comma separated ids. Ex: 2,1,3): ")
            try:
                dices_to_keep = dices_to_keep and list(map(int, dices_to_keep.split(','))) or []
                self.saved_dices = [all_dices[index - 1] for index in dices_to_keep]
                dices_to_roll = self.max_dices - len(self.saved_dices)
            except Exception:
                print(f"  Please select a valid dice combo  ".center(self.width, 'x'))
                dices_to_keep = None
        return dices_to_roll
