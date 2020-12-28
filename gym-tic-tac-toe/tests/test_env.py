from gym_tic_tac_toe.envs import TicTacToeEnv
from gym_tic_tac_toe.envs.tic_tac_toe_env import Xt, Ot, St, Pix

import unittest
import numpy as np


class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.env = TicTacToeEnv()

    def test_state_from_string(self):
        state_string = [
            '_XO',
            'O_X',
            '___'
        ]
        state_arr = np.array([
            [St, Xt, Ot],
            [Ot, St, Xt],
            [St, St, St]
        ])

        self.env.set_state(state_string)

        internal_state = self.env.state

        np.testing.assert_array_equal(state_arr, internal_state)

    def test_player_swap(self):
        self.env.reset()
        player_1 = self.env.player.string

        self.env.reset()
        player_2 = self.env.player.string

        self.assertNotEqual(player_1, player_2)

    def test_not_done(self):
        state_string = [
            '_XO',
            'O_X',
            '___'
        ]

        self.env.set_state(state_string)

        _, _, is_done, _ = self.env.step(0)

        self.assertFalse(is_done)

    def test_done_draw(self):
        state_string = [
            '_XO',
            'OXX',
            'XOO'
        ]

        self.env.set_state(state_string)

        _, _, is_done, _ = self.env.step(0)

        self.assertTrue(is_done)

    def test_done_draw_no_step(self):
        state_string = [
            'OXO',
            'OXX',
            'XOO'
        ]

        self.env.set_state(state_string)
        self.assertTrue(self.env.is_done)

    def test_x_win(self):
        state_string = [
            'XOO',
            '__O',
            'OOX'
        ]

        next_state_string = [
            'XOO',
            '_XO',
            'OOX'
        ]

        self.env.set_state(state_string)
        self.env.player = Pix.X
        self.env.rewards_for = Pix.X

        next_state, reward, is_done, _ = self.env.step(4)

        self.assertGreater(reward, 0)
        self.assertTrue(is_done)

        self.env.set_state(next_state_string)
        next_state_label = self.env.state

        np.testing.assert_array_equal(next_state, next_state_label)

    def test_x_loses(self):
        state_string = [
            'XOO',
            '__O',
            'OOX'
        ]

        self.env.set_state(state_string)
        self.env.player = Pix.O
        self.env.rewards_for = Pix.X

        _, reward, is_done, _ = self.env.step(4)

        self.assertLess(reward, 0)
        self.assertTrue(is_done)

    def test_initial_state(self):
        initial_state = self.env.reset().copy()
        self.env.player = Pix.X
        next_state, _, _, _ = self.env.step(0)

        initial_state_label = np.array([[St, St, St], [St, St, St], [St, St, St]])
        next_state_label = np.array([[Xt, St, St], [St, St, St], [St, St, St]])

        np.testing.assert_array_equal(initial_state, initial_state_label)
        np.testing.assert_array_equal(next_state, next_state_label)

    def test_illegal_action(self):
        state_string = [
            'XOO',
            '__O',
            'OOX'
        ]

        self.env.set_state(state_string)

        _, _, _, info = self.env.step(0)

        self.assertIsNotNone(info)


if __name__ == '__main__':
    unittest.main()
