import unittest
import numpy.testing as npt
from dominion_basics import *
from grid import *
from dominion import Dominion

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






if __name__ == "__main__":
    unittest.main()
