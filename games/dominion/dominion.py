import numpy as np
import sys
from dominion_basics import *
from grid import *
sys.path.append("../..")
from game import Game

# The state of this game has some hidden information that will be difficult to translate into the game.
# One player can see the cards in his hand. He is only aware of the number of cards in his opponents hand.
# 
class Dominion(Game):

    def get_initial_state(self):
        """Initialize first state and randomize which cards are part of the setup."""
        s0 = np.zeros((CARD_ROWS, CARD_COLS, STATE_LEVELS))
        return fill_supply(s0)

    # Observe what all the legal actions are in the current state
    # Previous this was done by returning a boolean matrix with trues in place of legal actions.
    def get_available_actions(self, s):
        """Returns boolean matrix with available actions"""
        # 7x7x3: layer 1: play card, 2: buy/gain card, 3: select card (Cellar, Chapel, et)
        return null

    def take_action(self, s, a):
        """Update the state based on the chosen action"""
        s = s.copy()
        raw = a.nonzero()
        assert len(raw[0]) == 1
        coord = (raw[0][0], raw[1][0])
        level = raw[2][0]
        p = int(s[CURRENT_PLAYER][TURN_STATE])
        if level == PLAY_ACTION:
            if coord != PASS_COORD:
                # obtain action card object
                card = CARD_MAP[coord]
                # move card from hand to play area
                s[coord][HAND+p] -= CARD_WEIGHT
                s[coord][PLAY_AREA+p] += CARD_WEIGHT
                if card.is_action():
                    # adjust action count
                    decrement_actions(s, inplace=True)
                    # adjust state
                    s = card.play_action(s, p)
                elif card.is_treasure():
                    s = card.play_treasure(s, p)
            # Check if we transition out of play phase
            # Create function for this
            if s[ACTION_PHASE][TURN_STATE] == 1 and (coord == PASS_COORD or s[ACTION_COORD][TURN_STATE] < CARD_WEIGHT*.5):
                s[ACTION_PHASE][TURN_STATE] = 0
                s[TREASURE_PHASE][TURN_STATE] = 1
            elif s[TREASURE_PHASE][TURN_STATE] == 1 and (coord == PASS_COORD or all_treasures_played(s, p)):
                s[TREASURE_PHASE][TURN_STATE] = 0
                s[BUY_PHASE][TURN_STATE] = 1
        elif level == BUY_CARD:
            # move card from supply to deck and discard
            if coord != PASS_COORD:
                card = CARD_MAP[coord]
                # reduce buys and money
                subtract_money(card.get_cost())
                decrement_buys(s, p)
                # Adjust supply and discard pile
                gain_card(s, coord, p)
                place_in_discard(s, coord, p)
            if coord == PASS_COORD or no_buys_left(s):
                # cleanup
                discard_hand(s, p)
                discard_in_play(s, p)
                draw_new_hand(s, p)
                # change player and state
        elif level == SELECT_CARD:
            pass
        else:
            raise Exception(f'Unknown level: {level}')
        return s

    def get_visible_state(self, s, p):
        """Remove the part of the state that is not visible to that player"""
        return null


    # TODO: Game should come to an end after 100 rounds. Track rounds for each player. Tie game at that point.
    def check_game_over(self, s):
        """Check if the game is over and if it is return rewards. Otherwise return None"""
        # TODO: Currently not accounting for 3 empty piles
        if s[PROVINCE_COORD][SUPPLY] == 0:
            # Sum score
            # TODO: add additional logic for other victory point cards (ie Gardens)
            scores = np.zeros(PLAYERS)
            for p in PLAYER_OFFSETS:
                scores[p] = score_deck(s[:,:,DECK+p])
            if scores[0] == scores[1]:
                return np.array([0,0])
            else:
                maxi = np.argmax(scores)
                scores[scores < scores.max()] = -1
                scores[maxi] = 1
            return scores


    def get_player(self, s):
        """Return which player is up to take a turn"""
        return s[CURRENT_PLAYER][TURN_STATE]

    def get_num_players(self):
    # For now lets only consider 2 player def get_num_players(self):
        return 2

    # Print a human-friendly version of the state
    def visualize(self, s):
        """Outputs to stdout a human readable version of the state"""
        print("X")


