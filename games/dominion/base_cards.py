# 2nd Edition
from dominion_basics import *

#class Artisan
#class Bandit
#class Bureaucrat
#class Cellar
#class Chapel
#class CouncilRoom

class Festival(ActionCard):
    def get_cost(self):
        return 5

    def play_action(self, s, p):
        add_actions(s, 2, inplace=True)
        add_buys(s, 1, inplace=True)
        add_money(s, 2, inplace=True)
        return s
