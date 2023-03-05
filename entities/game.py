import random
from display.dice import Dice
from display.score_card import ScoreCardDisplay
from display.table import Display
from entities.player import Player
from entities.rules import Rule, CountOnlyOne, CountOnlyTwo, CountOnlyThree, CountOnlyFour, ThreeOfAKind, FourOfAKind, FourInARow, Anything
from entities.score_card import ScoreCard


class Game:
    def __init__(self) -> None:
        self._rules: list(Rule) = [
            CountOnlyOne(),
            CountOnlyTwo(),
            CountOnlyThree(),
            CountOnlyFour(),
            ThreeOfAKind(),
            FourOfAKind(),
            FourInARow(),
            Anything(),
        ]
        self.players = [
            Player(name="John", score_card=ScoreCard(self._rules)),
            Player(name="Bob", score_card=ScoreCard(self._rules))
        ]
        self.round = 0
        self.width = 100
    
    def add_rule(self, rule: Rule):
        self._rules.append(rule)
        return self

    def add_player(self, player_name):
        score_card = ScoreCard(self._rules)
        player = Player(player_name, score_card)
        self.players.append(player)

    def start(self):
        while not self.over():
            self.next_round()
            self.round = self.round + 1
        
        Display(
            *[ScoreCardDisplay(player.score_card, title=f"{player.name} Scorecard") for player in self.players]
        ).display()
        
        
    def over(self) -> bool:
        return self.round == 8
    
    def next_round(self):
        print(f"Round {self.round}".center(self.width, "=") + "\n")
        for player in self.players:
            self.next_turn(player)

    def next_turn(self, player: Player):
        print(f"{player.name} Turn".center(self.width, "-") + "\n")
        player.saved_dices = []
        player.dices_to_roll = 4
        for i in range(3):
            rolled_dices = []
            if player.dices_to_roll:
                rolled_dices = [random.randint(1, 6) for i in range(player.dices_to_roll)]
            
                display_dices = []
                if player.saved_dices:
                    display_dices.append(Dice(player.saved_dices, name=f"Turn {i + 1}, Saved Dices..."))
                display_dices.append(Dice(rolled_dices, name=f"Turn {i + 1}, Rolled {player.dices_to_roll} Dices..."))
                tg = Display(*display_dices)
                tg.display()

            all_dices = [*player.saved_dices, *rolled_dices] 
            if rolled_dices and i + 1 < 3:
                tg = Display(Dice(all_dices, name=f"Turn {i + 1}, Select dices to keep:", include_id_header=True))
                tg.display()
                dices_to_keep = input()
                if dices_to_keep:
                    dices_to_keep = list(map(int, dices_to_keep.split(',')))
                    player.saved_dices = [all_dices[index - 1] for index in dices_to_keep]
                    player.dices_to_roll = 4 - len(player.saved_dices)
                else:
                    player.saved_dices = []
                    player.dices_to_roll = 4
            else:
                self.mark_rule(player, all_dices)
                Display(ScoreCardDisplay(player.score_card, title="Your score")).display()
                break

        print(f"End {player.name} Turn".center(self.width, "-") + "\n")
        return
    
    def choose_score(self, player: Player, all_dices: list[int]):
        choice = None
        while choice is None:
            Display(Dice(all_dices, name=f"Final dices:", include_id_header=True)).display()
            possible_scores = Player.generate_possible_scores(self._rules, all_dices)
            Display(
                ScoreCardDisplay(player.score_card, title="Your Score"),
                ScoreCardDisplay(possible_scores, title="Choose Your Next Score")
            ).display()
            try:
                choice = int(input())
                self._rules[choice] # Test index
            except Exception:
                print(f"Invalid Score choosen, please pick a valid score.".center(self.width, "."))
                choice = None
        return choice
    
    def mark_rule(self, player, all_dices:list[int]):
        while True:
            rule = None
            try:
                score_choice = self.choose_score(player, all_dices)
                rule = self._rules[score_choice]
                player.score_card.mark_rule(rule.name, rule.get_score(all_dices))
                Display(ScoreCardDisplay(player.score_card, title="Your score")).display()
                break
            except ValueError as e:
                print("\n")
                print(f"You have already selected [{rule.name}], please select a different score".center(self.width, '.'))
                

def run():
    g = Game()
    g.start()

run()