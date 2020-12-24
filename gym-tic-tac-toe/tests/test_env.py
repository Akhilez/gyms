from gym_tic_tac_toe.envs import TicTacToeEnv
from gym_tic_tac_toe.envs.tic_tac_toe_env import Xt, Ot, St

import unittest
import numpy as np


env = TicTacToeEnv()

state = env.reset()
reward = env.step(4)


class TestSum(unittest.TestCase):

    def setUp(self):
        self.env = TicTacToeEnv()

    def test_empty_state(self):
        empty_state = np.zeros((3, 3, 3))
        init_state = self.env.reset()

        np.testing.assert_array_equal(empty_state, init_state)

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

        _, _, is_done = self.env.step(0)

        self.assertFalse(is_done)


if __name__ == '__main__':
    unittest.main()
