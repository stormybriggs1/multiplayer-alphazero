import unittest
import numpy as np
import numpy.testing as npt
from dominion_basics import *
from dominion import Dominion

class TestDominionBasics(unittest.TestCase):
    d = Dominion()

    def test_add_money(self):
        s0 = self.d.get_initial_state()
        self.assertEqual(s0[MONEY_COORDS[0]][TURN_STATE], 0)
        copy = np.copy(s0)
        s1 = add_money(s0, 1)
        npt.assert_array_equal(s0, copy)
        self.assertAlmostEqual(s1[MONEY_COORDS[0]][TURN_STATE], CARD_WEIGHT, places=5)

    def test_add_money_overflow(self):
        s0 = self.d.get_initial_state()
        s1 = add_money(s0, 11)
        self.assertAlmostEqual(s1[MONEY_COORDS[0]][TURN_STATE], 1.0, places=5)
        self.assertAlmostEqual(s1[MONEY_COORDS[1]][TURN_STATE], CARD_WEIGHT, places=5)
       
    def test_add_money_full(self):
        s0 = self.d.get_initial_state()
        s1 = add_money(s0, 51)
        for coord in MONEY_COORDS:
            self.assertAlmostEqual(s1[coord][TURN_STATE], 1.0, places=5)
        self.assertAlmostEqual(s1[1,5,TURN_STATE], 0, places=5)

    def test_add_money_inplace(self):
        s0 = self.d.get_initial_state()
        copy = np.copy(s0)
        add_money(s0, 2, inplace=True)
        self.assertAlmostEqual(s0[MONEY_COORDS[0]][TURN_STATE], CARD_WEIGHT*2, places=5)
        self.assertAlmostEqual(copy[MONEY_COORDS[0]][TURN_STATE], 0, places=5)

    def test_subtract_money(self):
        s0 = self.d.get_initial_state()
        self.assertEqual(s0[MONEY_COORDS[0]][TURN_STATE], 0)
        s0[MONEY_COORDS[0]][TURN_STATE] = CARD_WEIGHT * 2
        copy = np.copy(s0)
        s1 = subtract_money(s0, 1)
        npt.assert_array_equal(s0, copy)
        self.assertAlmostEqual(s1[MONEY_COORDS[0]][TURN_STATE], CARD_WEIGHT, places=5)

    def test_subtract_money_overflow(self):
        s0 = self.d.get_initial_state()
        s1 = add_money(s0, 11)
        s2 = subtract_money(s1, 8)
        self.assertAlmostEqual(s1[MONEY_COORDS[0]][TURN_STATE], 1.0, places=5)
        self.assertAlmostEqual(s1[MONEY_COORDS[1]][TURN_STATE], CARD_WEIGHT, places=5)
        self.assertAlmostEqual(s2[MONEY_COORDS[1]][TURN_STATE], 0.0, places=5)
        self.assertAlmostEqual(s2[MONEY_COORDS[0]][TURN_STATE], 3*CARD_WEIGHT, places=5)

    def test_subtract_money_inplace(self):
        s0 = self.d.get_initial_state()
        copy = np.copy(s0)
        add_money(s0, 3, inplace=True)
        subtract_money(s0, 2, inplace=True)
        self.assertAlmostEqual(s0[MONEY_COORDS[0]][TURN_STATE], CARD_WEIGHT, places=5)
        self.assertAlmostEqual(copy[MONEY_COORDS[0]][TURN_STATE], 0, places=5)

    def test_add_actions(self):
        s0 = self.d.get_initial_state()
        add_actions(s0, 2, inplace=True)
        self.assertAlmostEqual(s0[ACTION_COORD][TURN_STATE], 2*ACTION_WEIGHT, places=5)
        decrement_actions(s0, inplace=True)
        self.assertAlmostEqual(s0[ACTION_COORD][TURN_STATE], ACTION_WEIGHT, places=5)
        add_actions(s0, 10, inplace=True)
        self.assertAlmostEqual(s0[ACTION_COORD][TURN_STATE], 1.0, places=5)

    def test_add_buys(self):
        s0 = self.d.get_initial_state()
        add_buys(s0, 1, inplace=True)
        self.assertAlmostEqual(s0[BUY_COORD][TURN_STATE], BUY_WEIGHT, places=5)
        decrement_buys(s0, inplace=True)
        self.assertAlmostEqual(s0[BUY_COORD][TURN_STATE], 0, places=5)
        decrement_buys(s0, inplace=True)
        self.assertAlmostEqual(s0[BUY_COORD][TURN_STATE], 0, places=5)
        add_buys(s0, 11, inplace=True)
        self.assertAlmostEqual(s0[BUY_COORD][TURN_STATE], 1, places=5)


if __name__ == "__main__":
    unittest.main()
