import unittest
import numpy.testing as npt
from dominion_basics import *
from grid import *
from dominion import Dominion
from collections import Counter

class TestGrid(unittest.TestCase):
    d = Dominion()

    def test_all_treasured_played(self):
        s = self.d.get_initial_state()
        p = 1
        s[ESTATE_COORDS[0]][HAND+p] = CARD_WEIGHT * 3
        self.assertTrue(all_treasures_played(s, p))
        s[COPPER_COORDS[0]][HAND+p] = CARD_WEIGHT * 2
        self.assertFalse(all_treasures_played(s, p))

    def test_gain_card(self):
        s0 = self.d.get_initial_state()
        p = 0
        s0[FESTIVAL_COORD][SUPPLY] = CARD_WEIGHT * 2
        self.assertAlmostEqual(s0[FESTIVAL_COORD][DECK+p], 0, places=5)
        s1 = s0.copy()
        gain_card(s1, FESTIVAL_COORD, p)
        self.assertAlmostEqual(s1[FESTIVAL_COORD][DECK+p], CARD_WEIGHT, places=5)
        self.assertAlmostEqual(s1[FESTIVAL_COORD][SUPPLY], CARD_WEIGHT, places=5)
        gain_card(s1, FESTIVAL_COORD, p)
        self.assertAlmostEqual(s1[FESTIVAL_COORD][DECK+p], 2 * CARD_WEIGHT, places=5)
        self.assertAlmostEqual(s1[FESTIVAL_COORD][SUPPLY], EMPTY, places=5)
        s2 = s1.copy()
        gain_card(s2, FESTIVAL_COORD, p)
        npt.assert_array_equal(s1, s2)

    def test_decrement_buys(self):
        s0 = self.d.get_initial_state()
        s0[BUY_COORD][TURN_STATE] = BUY_WEIGHT
        decrement_buys(s0)
        self.assertAlmostEqual(s0[BUY_COORD][TURN_STATE], 0, places=5)
        s1 = s0.copy()
        decrement_buys(s1)
        npt.assert_array_equal(s0, s1)

    def test_no_buys_left(self):
        s0 = self.d.get_initial_state()
        s0[BUY_COORD][TURN_STATE] = BUY_WEIGHT
        self.assertFalse(no_buys_left(s0))
        s0[BUY_COORD][TURN_STATE] = 0
        self.assertTrue(no_buys_left(s0))

    def test_discard_hand(self):
        s = self.d.get_initial_state()
        p = 1
        s[COPPER_COORDS[0]][HAND+p] = 3 * CARD_WEIGHT
        s[ESTATE_COORDS[0]][HAND+p] = 2 * CARD_WEIGHT
        self.assertAlmostEqual(s[COPPER_COORDS[0]][DISCARD+p], 0, places=5)
        discard_hand(s, p)
        self.assertAlmostEqual(s[COPPER_COORDS[0]][DISCARD+p], 3 * CARD_WEIGHT, places=5)
        self.assertAlmostEqual(s[COPPER_COORDS[0]][HAND+p], 0, places=5)
        self.assertAlmostEqual(s[ESTATE_COORDS[0]][DISCARD+p], 2 * CARD_WEIGHT, places=5)
        self.assertAlmostEqual(s[ESTATE_COORDS[0]][HAND+p], 0, places=5)

    def test_draw_one_card(self):
        s = self.d.get_initial_state()
        p = 0
        s[:,:,AVAILABLE_DECK+p] = 0
        s[COPPER_COORDS[0]][AVAILABLE_DECK+p] = CARD_WEIGHT * 7
        s[ESTATE_COORDS[0]][AVAILABLE_DECK+p] = CARD_WEIGHT * 3
        s[:,:,HAND+p] = 0
        # Draw one card over and over should not be 100% same card
        counter = Counter()
        for _ in range(100):
            s1 = s.copy()
            draw_card(s1, p)
            self.assertAlmostEqual(s1[:,:,HAND+p].sum(), CARD_WEIGHT, places=5)
            if s1[COPPER_COORDS[0]][HAND+p] > 0:
                counter['copper'] += 1
            elif s1[ESTATE_COORDS[0]][HAND+p] > 0:
                counter['estate'] += 1
            else:
                self.fail('No card drawn')
        self.assertTrue(counter['copper'] < 100)
        self.assertTrue(counter['estate'] < 100)

        # Draw 10 cards from a deck of 10. All 10 cards should be drawn
    def test_draw_10_cards(self):
        s = self.d.get_initial_state()
        p = 0
        s[:,:,AVAILABLE_DECK+p] = 0
        s[COPPER_COORDS[0]][AVAILABLE_DECK+p] = CARD_WEIGHT * 5
        s[SILVER_COORDS[0]][AVAILABLE_DECK+p] = CARD_WEIGHT
        s[ESTATE_COORDS[0]][AVAILABLE_DECK+p] = CARD_WEIGHT * 3
        s[FESTIVAL_COORD][AVAILABLE_DECK] = CARD_WEIGHT
        s[:,:,HAND+p] = 0
        for _ in range(10):
            draw_card(s, p)
        self.assertAlmostEqual(s[:,:,AVAILABLE_DECK+p].sum(), 0, places=5)
        self.assertAlmostEqual(s[COPPER_COORDS[0]][HAND+p], CARD_WEIGHT*5, places=5)
        self.assertAlmostEqual(s[SILVER_COORDS[0]][HAND+p], CARD_WEIGHT, places=5)
        self.assertAlmostEqual(s[ESTATE_COORDS[0]][HAND+p], CARD_WEIGHT*3, places=5)
        self.assertAlmostEqual(s[FESTIVAL_COORD][HAND+p], CARD_WEIGHT, places=5)



if __name__ == "__main__":
    unittest.main()
