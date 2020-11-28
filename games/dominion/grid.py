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

def score_deck(d):
    return int((d * VICTORY_GRID).sum())


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

