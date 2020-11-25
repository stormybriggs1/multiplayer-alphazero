import unittest
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


if __name__ == "__main__":
    unittest.main()
