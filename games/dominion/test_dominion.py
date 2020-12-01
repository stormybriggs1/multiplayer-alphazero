import unittest
import numpy.testing as npt
from dominion_basics import *
from grid import score_deck
from dominion import Dominion

class TestDominion(unittest.TestCase):
    d = Dominion()

    def test_constant(self):
        self.assertEqual(SUPPLY, 0)

    def test_check_game_over(self):
        s0 = self.d.get_initial_state()
        self.assertEqual(self.d.check_game_over(s0), None)

        tie = np.copy(s0)
        tie[PROVINCE_COORD][SUPPLY] = 0
        self.assertEqual(score_deck(tie[:,:,DECK+0]), 3)
        npt.assert_array_equal(self.d.check_game_over(tie), np.zeros(2))

        p0win = np.copy(tie)
        p0win[DUCHY_COORD][DECK+0] = 1 * CARD_WEIGHT
        self.assertEqual(score_deck(p0win[:,:,DECK+0]), 6)
        npt.assert_array_equal(self.d.check_game_over(p0win), np.array([1,-1]))

        p1win = np.copy(tie)
        p1win[PROVINCE_COORD][DECK+1] = 1 * CARD_WEIGHT
        self.assertEqual(score_deck(p1win[:,:,DECK+1]), 9)
        npt.assert_array_equal(self.d.check_game_over(p1win), np.array([-1,1]))

    def test_take_action_festival(self):
        s0 = self.d.get_initial_state()
        s0[CURRENT_PLAYER][TURN_STATE] = 0
        s0[FESTIVAL_COORD][HAND] = CARD_WEIGHT
        s0[ACTION_PHASE][TURN_STATE] = 1
        s0[ACTION_COORD][TURN_STATE] = ACTION_WEIGHT
        a = np.zeros((CARD_ROWS, CARD_COLS, ACTION_LEVELS), dtype=bool)
        a[FESTIVAL_COORD][PLAY_ACTION] = True
        copy = s0.copy()
        s1 = self.d.take_action(s0, a)
        npt.assert_array_equal(s0, copy) # Original state is unchanged
        self.assertAlmostEqual(s1[ACTION_PHASE][TURN_STATE], 1, places=5)
        self.assertAlmostEqual(s1[CURRENT_PLAYER][TURN_STATE], 0, places=5)
        self.assertAlmostEqual(s1[FESTIVAL_COORD][HAND], 0, places=5)
        self.assertAlmostEqual(s1[FESTIVAL_COORD][PLAY_AREA], CARD_WEIGHT, places=5)
        self.assertAlmostEqual(s1[ACTION_COORD][TURN_STATE], ACTION_WEIGHT * 2, places=5)
        self.assertAlmostEqual(s1[MONEY_COORDS[0]][TURN_STATE], MONEY_WEIGHT * 2, places=5)
        self.assertAlmostEqual(s1[BUY_COORD][TURN_STATE], s0[BUY_COORD][TURN_STATE] + BUY_WEIGHT, places=5)

    def test_play_treasures(self):
        s0 = self.d.get_initial_state()
        p = 1
        s0[COPPER_COORDS[0]][HAND+p] = CARD_WEIGHT*3
        s0[SILVER_COORDS[0]][HAND+p] = CARD_WEIGHT
        s0[GOLD_COORDS[0]][HAND+p] = CARD_WEIGHT
        s0[ACTION_PHASE][TURN_STATE] = 0
        s0[TREASURE_PHASE][TURN_STATE] = 1
        s0[CURRENT_PLAYER][TURN_STATE] = p
        # play each treasure and observe money increase
        play_copper = np.zeros((CARD_ROWS, CARD_COLS, ACTION_LEVELS), dtype=bool)
        play_silver = play_copper.copy()
        play_gold = play_copper.copy()
        finish_treasures = play_copper.copy()
        play_copper[COPPER_COORDS[0]][PLAY_ACTION] = True 
        play_silver[SILVER_COORDS[0]][PLAY_ACTION] = True
        play_gold[GOLD_COORDS[0]][PLAY_ACTION] = True
        finish_treasures[PASS_COORD][PLAY_ACTION] = True
        print("play copper")
        s1 = self.d.take_action(s0, play_copper)
        print("after play")
        self.assertAlmostEqual(s1[COPPER_COORDS[0]][HAND+p], CARD_WEIGHT*2, places=5)
        self.assertAlmostEqual(s1[MONEY_COORDS[0]][TURN_STATE], MONEY_WEIGHT, places=5)
        self.assertAlmostEqual(s1[TREASURE_PHASE][TURN_STATE], 1, places=5)
        s2 = self.d.take_action(s1, play_silver)
        self.assertAlmostEqual(s2[SILVER_COORDS[0]][HAND+p], 0, places=5)
        self.assertAlmostEqual(s2[MONEY_COORDS[0]][TURN_STATE], MONEY_WEIGHT*3, places=5)
        self.assertAlmostEqual(s2[TREASURE_PHASE][TURN_STATE], 1, places=5)
        s3 = self.d.take_action(s2, play_gold)
        self.assertAlmostEqual(s3[GOLD_COORDS[0]][HAND+p], 0, places=5)
        self.assertAlmostEqual(s3[MONEY_COORDS[0]][TURN_STATE], MONEY_WEIGHT*6, places=5)
        self.assertAlmostEqual(s3[TREASURE_PHASE][TURN_STATE], 1, places=5)
        s4 = self.d.take_action(s3, finish_treasures)
        self.assertAlmostEqual(s4[TREASURE_PHASE][TURN_STATE], 0, places=5)
        self.assertAlmostEqual(s4[BUY_PHASE][TURN_STATE], 1, places=5)
        s4 = self.d.take_action(s3, play_copper)
        s5 = self.d.take_action(s4, play_copper)
        self.assertAlmostEqual(s5[COPPER_COORDS[0]][HAND+p], 0, places=5)
        self.assertAlmostEqual(s5[MONEY_COORDS[0]][TURN_STATE], MONEY_WEIGHT*8, places=5)
        self.assertAlmostEqual(s5[TREASURE_PHASE][TURN_STATE], 0, places=5)
        self.assertAlmostEqual(s5[BUY_PHASE][TURN_STATE], 1, places=5)
        





    def test_buy(self):
        pass

    def test_action_transitions(self):
        pass
        


if __name__ == "__main__":
    unittest.main()
