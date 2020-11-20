from dominion_basics import *

class VictoryCard(Card):
    def __init__(self):
        pass

class Province(VictoryCard):
    def is_stateless_victory_card(self):
        return True

    def get_victory_points(self, s):
        return 6

    def get_cost(self):
        return 8

class Duchy(VictoryCard):
    def is_stateless_victory_card(self):
        return True

    def get_victory_points(self, s):
        return 3

    def get_cost(self):
        return 5

class Estate(VictoryCard):
    def is_stateless_victory_card(self):
        return True

    def get_victory_points(self, s):
        return 1

    def get_cost(self):
        return 2

class Curse(Card):
    def is_stateless_victory_card(self):
        return True

    def get_victory_points(self, s):
        return -1

