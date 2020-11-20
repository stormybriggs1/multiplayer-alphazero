import numpy as np

PLAYERS = 2
CARD_ROWS = 7
CARD_COLS = 7
STATE_LEVELS = 13
CARD_WEIGHT = 0.1
ACTION_WEIGHT = 0.1
BUY_WEIGHT = 0.1
MONEY_WEIGHT = 0.1

# State Levels
PLAYER_OFFSETS = [0,1]
SUPPLY = 0
DECK = 1 # +1 for 2nd player
HAND = 3 # +1
DISCARD = 5 # +1
AVAILABLE_DECK = 7 # +1
PLAY_AREA = 9 # +1
TRASH = 11
TURN_STATE = 12

# Card coordinates
PROVINCE_COORD = (0,0)
DUCHY_COORD = (0,1)
ESTATE_COORDS = [(0,2), (0,3)]
CURSES_COORD = (0,4)
GOLD_COORDS = [(0,5), (0,6), (1,0)]
SILVER_COORDS = [(1,1), (1,2), (1,3), (1,4)]
COPPER_COORDS = [(1,5), (1,6), (2,0), (2,1), (2,2), (2,3)]
FESTIVAL_COORD = (2,4)
PASS_COORD = (6,6)

# Turn state coordinates
TRUE = 1.0
FALSE = 0.0
CURRENT_PLAYER = (0,0)
ACTION_PHASE = (0,1)
TREASURE_PHASE = (0,2)
BUY_PHASE = (0,3)
ACTION_COORD = (1,0)
#ACTION_OVERFLOW_COORD = (1,1)
BUY_COORD = (1,2)
#BUY_OVERFLOW_COORD = (1,3)
MONEY_COORDS = [(2,0), (2,1), (2,2), (2,3), (2,4)]

# Action Levels
PLAY_ACTION = 0
BUY_CARD = 1
SELECT_CARD = 2
ACTION_LEVELS = 3

def fill_supply(s):
    # 8 Cards in each victory pile
    for coord in [PROVINCE_COORD, DUCHY_COORD, ESTATE_COORDS[0]]:
        s[coord][SUPPLY] = 8 * CARD_WEIGHT
    # 3 estates in each players deck
    for p in PLAYER_OFFSETS:
        s[ESTATE_COORDS[0]][DECK+p] = 3 * CARD_WEIGHT
        s[COPPER_COORDS[0]][DECK+p] = 7 * CARD_WEIGHT
    # 10 curses
    s[CURSES_COORD][SUPPLY] = 10 * CARD_WEIGHT
    # 30 gold
    for coord in GOLD_COORDS:
        s[coord][SUPPLY] = 10 * CARD_WEIGHT
    # 40 silver
    for coord in SILVER_COORDS:
        s[coord][SUPPLY] = 10 * CARD_WEIGHT
    # 46 copper in supply
    copper = 46
    for coord in COPPER_COORDS:
        if copper >= 10:
            s[coord][SUPPLY] = 10 * CARD_WEIGHT
            copper -= 10
        else:
            s[coord][SUPPLY] = copper * CARD_WEIGHT
            copper = 0

    return s

def add_money(s, amount, inplace=False):
    if not inplace:
        s = np.copy(s)
    weighted_amount = amount * MONEY_WEIGHT
    for coord in MONEY_COORDS:
        coord_value = s[coord][TURN_STATE]
        if coord_value < 1.0:
            diff = min(1 - coord_value, weighted_amount)
            weighted_amount -= diff
            s[coord][TURN_STATE] += diff
            if weighted_amount < 0.0001:
                break
    if not inplace:
        return s
            

def subtract_money(s, amount, inplace=False):
    if not inplace:
        s = np.copy(s)
    weighted_amount = amount * MONEY_WEIGHT
    for coord in list(reversed(MONEY_COORDS)):
        coord_value = s[coord][TURN_STATE]
        if coord_value > 0.0:
            diff = min(coord_value, weighted_amount)
            weighted_amount -= diff
            s[coord][TURN_STATE] -= diff
            if weighted_amount < 0.0001:
                break
    if not inplace:
        return s

def add_actions(s, actions, inplace=False):
    if not inplace:
        s = np.copy(s)
    weighted_amount = actions * ACTION_WEIGHT
    s[ACTION_COORD][TURN_STATE] = min(weighted_amount + s[ACTION_COORD][TURN_STATE], 1.0)
    if not inplace:
        return s

def decrement_actions(s, inplace=False):
    if not inplace:
        s = np.copy(s)
    s[ACTION_COORD][TURN_STATE] = max(s[ACTION_COORD][TURN_STATE] - ACTION_WEIGHT, 0)
    if not inplace:
        return s

def add_buys(s, buys, inplace=False):
    if not inplace:
        s = np.copy(s)
    weighted_amount = buys * BUY_WEIGHT
    s[BUY_COORD][TURN_STATE] = min(weighted_amount + s[BUY_COORD][TURN_STATE], 1.0)
    if not inplace:
        return s

def decrement_buys(s, inplace=False):
    if not inplace:
        s = np.copy(s)
    s[BUY_COORD][TURN_STATE] = max(s[BUY_COORD][TURN_STATE] - BUY_WEIGHT, 0)
    if not inplace:
        return s

def all_treasures_played(s, p):
    return None


class Card:
    def get_cost(self):
        return 0

    def is_action(self):
        return False

    def is_treasure(self):
        return False

    # Assume that somewhere else is the state adjusted for moving the card to the right place.
    def play_action(self, s, p):
        raise Exception("Not Action")

    def play_treasure(self, s, p):
        raise Exception("Not Treasure")

    def is_stateless_victory_card(self):
        return False

    def get_victory_points(self, s):
        return 0

class ActionCard(Card):
    def is_action(self):
        return True
