from numpy.random import choice
from base_cards import *
from dominion_basics import *
from treasure_cards import *
from victory_cards import *


# Card map
CARD_MAP = {}

CARD_MAP[PROVINCE_COORD] = Province()
CARD_MAP[DUCHY_COORD] = Duchy()
for coord in ESTATE_COORDS:
    CARD_MAP[coord] = Estate()
CARD_MAP[CURSES_COORD] = Curse()
for coord in GOLD_COORDS:
    CARD_MAP[coord] = Gold()
for coord in SILVER_COORDS:
    CARD_MAP[coord] = Silver()
for coord in COPPER_COORDS:
    CARD_MAP[coord] = Copper()

# Next up
# Village, Smithy, Festival, Laboratory, Market, Witch, Garden, Workshop, Merchant, Remodel, Cellar, Chapel
CARD_MAP[FESTIVAL_COORD] = Festival()
# Need to work through keeping state of buy phase, action phase, move the cards around outside of an action on a card

def fill_victory_grid():
    vgrid = np.zeros((CARD_ROWS, CARD_COLS))
    for coord, card in CARD_MAP.items():
        if card.is_stateless_victory_card():
            vgrid[coord] = card.get_victory_points(None)
    vgrid /= CARD_WEIGHT
    return vgrid

# Victory grid
VICTORY_GRID = fill_victory_grid()

def fill_treasure_mask():
    tmask = np.ones((CARD_ROWS, CARD_COLS), dtype=bool)
    for coord, card in CARD_MAP.items():
        if card.is_treasure():
            tmask[coord] = False
    return tmask

TREASURE_MASK = fill_treasure_mask()

def all_treasures_played(s, p):
    masked = np.ma.masked_array(s[:,:,HAND+p], TREASURE_MASK)
    return masked.sum() == 0

def fill_supply(s):
    # 8 Cards in each victory pile
    for coord in [PROVINCE_COORD, DUCHY_COORD, ESTATE_COORDS[0]]:
        s[coord][SUPPLY] = 8 * CARD_WEIGHT
    # 3 estates in each players deck
    for p in PLAYER_OFFSETS:
        s[ESTATE_COORDS[0]][DECK+p] = 3 * CARD_WEIGHT
        s[COPPER_COORDS[0]][DECK+p] = 7 * CARD_WEIGHT
        s[:,:,AVAILABLE_DECK+p] = s[:,:,DECK+p]
        draw_new_hand(s, p)
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



def score_deck(d):
    return int((d * VICTORY_GRID).sum())

def from_hand_to_play(s, p):
    s[coord][HAND+p] -= CARD_WEIGHT
    s[coord][PLAY_AREA+p] += CARD_WEIGHT

def is_action_phase(s):
    return s[ACTION_PHASE][TURN_STATE] == 1

def end_action_phase(s):
    s[ACTION_PHASE][TURN_STATE] = 0
    s[TREASURE_PHASE][TURN_STATE] = 1

def is_treasure_phase(s):
    return s[TREASURE_PHASE][TURN_STATE] == 1

def end_treasure_phase(s):
    s[TREASURE_PHASE][TURN_STATE] = 0
    s[BUY_PHASE][TURN_STATE] = 1

def gain_card(s, coord, p):
    """Change the state by adding one copy of card at coord to player p's deck"""
    if s[coord][SUPPLY] > 0:
        s[coord][SUPPLY] -= CARD_WEIGHT
        if s[coord][SUPPLY] <= 0:
            s[coord][SUPPLY] = EMPTY
        s[coord][DECK+p] += CARD_WEIGHT

def place_in_discard(s, coord, p):
    """Add this card to player p's discard. Assumes removal from elsewhere is taken care of."""
    s[coord][DISCARD+p] += CARD_WEIGHT

def decrement_buys(s):
    """Decrease buys in turn state by one"""
    if s[BUY_COORD][TURN_STATE] > 0:
        s[BUY_COORD][TURN_STATE] -= BUY_WEIGHT

def no_buys_left(s):
    """Returns true if number of buys is zero or false otherwise"""
    return s[BUY_COORD][TURN_STATE] <= 0

def discard_hand(s, p):
    """Move all cards from hand to discard pile"""
    s[:,:,DISCARD+p] += s[:,:,HAND+p]
    s[:,:,HAND+p] = 0

def discard_in_play(s, p):
    """Move all cards in play into discard pile"""
    s[:,:,DISCARD+p] += s[:,:,PLAY_AREA+p]
    s[:,:,PLAY_AREA+p] = 0

def draw_card(s, p):
    # check if draw pile is empty, if it is move discard pile to draw pile
    if s[:,:,AVAILABLE_DECK+p].sum() == 0:
        s[:,:,AVAILABLE_DECK+p] += s[:,:,DISCARD+p]
        s[:,:,DISCARD+p] = 0
    # calculate row probabilities
    row_prob = s[:,:,AVAILABLE_DECK+p].sum(axis=1) / s[:,:,AVAILABLE_DECK+p].sum()
    # choose random row
    row = choice(np.arange(CARD_ROWS), 1, p=row_prob)[0]
    # choose column probabilities
    col_prob = s[row,:,AVAILABLE_DECK+p] / s[row,:,AVAILABLE_DECK+p].sum()
    # choose random column
    col = choice(np.arange(CARD_COLS), 1, p=col_prob)[0]
    # move card from draw pile to hand
    s[row, col, AVAILABLE_DECK+p] -= CARD_WEIGHT
    s[row, col, HAND+p] += CARD_WEIGHT

def draw_new_hand(s, p):
    for _ in range(5):
        draw_card(s, p)

def end_turn(s):
    s[CURRENT_PLAYER][TURN_STATE] = (s[CURRENT_PLAYER][TURN_STATE] + 1) % 2
    s[ACTION_PHASE][TURN_STATE] = 1
    s[TREASURE_PHASE][TURN_STATE] = 0
    s[BUY_PHASE][TURN_STATE] = 0
