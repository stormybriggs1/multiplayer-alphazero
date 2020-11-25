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



