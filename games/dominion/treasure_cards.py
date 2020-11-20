from dominion_basics import *

class TreasureCard(Card):
    def is_treasure(self):
        return True

class Gold(TreasureCard):
    def get_cost(self):
        return 6

    def play_treasure(self, s, p):
        return add_money(s, 3)


class Silver(TreasureCard):
    def get_cost(self):
        return 3

    def play_treasure(self, s, p):
        return add_money(s, 2)

class Copper(TreasureCard):
    def play_treasure(self, s, p):
        return add_money(s, 1)
