from gym_nine_mens_morris.envs import NineMensMorrisEnv

import unittest
import numpy as np

from gym_nine_mens_morris.envs.nine_mens_morris_env import Pix

St = Pix.S.tup
Wt = Pix.W.tup
Bt = Pix.B.tup

Ss = Pix.S.string
Ws = Pix.W.string
Bs = Pix.B.string


class TestNineMensMorris(unittest.TestCase):

    def setUp(self):
        self.env = NineMensMorrisEnv()

    def test_state_from_string(self):
        state_string = [
            # 123456789012
            'W-----O-----O',  # 0
            '| O---B---W |',  # 1
            '| | W-O-B | |',  # 2
            'B-O-O   W-O-O',  # 3
            '| | B-O-O | |',  # 4
            '| O---O---B |',  # 5
            'W-----O-----O',  # 6
        ]
        state_arr = np.array([
            # Outer layer
            [
                [Wt, St, St, Wt],  # Corners
                [Bt, St, St, St]  # Edges
            ],

            # Middle layer
            [
                [St, Wt, Bt, St],  # Corners
                [St, Bt, St, St]  # Edges
            ],

            # Inner layer
            [
                [Wt, Bt, St, Bt],  # Corners
                [St, St, Wt, St]  # Edges
            ],
        ])

        self.env.set_state(state_string, [0, 0, 0, 0])
        internal_state = self.env.board

        np.testing.assert_array_equal(state_arr, internal_state)

    def test_player_swap_on_reset(self):
        self.env.reset()
        player_1 = self.env.player.string

        self.env.reset()
        player_2 = self.env.player.string

        self.assertNotEqual(player_1, player_2)

    def test_player_swap_on_step(self):
        self.env.reset()
        player_1 = self.env.player.string

        self.env.step((0, 0, 0))
        player_2 = self.env.player.string

        self.assertNotEqual(player_1, player_2)

    def test_not_done(self):
        self.env.reset()

        _, _, is_done, _ = self.env.step((0, 0, 0))

        self.assertFalse(is_done)

        self.env.mens = np.array([0, 0, 0, 8])
        self.assertFalse(self.env.is_done)

    def test_done(self):
        self.env.reset()

        self.env.mens = np.array([0, 0, 8, 9])

        _, _, is_done, _ = self.env.step((0, 0, 0))

        self.assertFalse(is_done)

    def test_not_killed(self):
        state_string = [
            # 123456789012
            'W-----O-----W',  # 0
            '| O---B---W |',  # 1
            '| | W-O-B | |',  # 2
            'B-O-O   W-O-O',  # 3
            '| | B-O-O | |',  # 4
            '| O---O---B |',  # 5
            'W-----O-----O',  # 6
        ]

        self.env.set_state(state_string, [3, 4, 0, 0])
        self.env.player = Pix.B
        self.env.opponent = Pix.W

        state, reward, is_done, info = self.env.step((0, 1, 1))

        self.assertEqual(reward, 0)
        self.assertEqual(list(self.env.mens), [3, 3, 0, 0])
        self.assertFalse(is_done)

    def test_killed_no_removed_piece(self):
        state_string = [
            # 123456789012
            'W-----O-----W',  # 0
            '| O---B---W |',  # 1
            '| | W-O-B | |',  # 2
            'B-O-O   W-O-O',  # 3
            '| | B-O-O | |',  # 4
            '| O---O---B |',  # 5
            'W-----O-----O',  # 6
        ]

        self.env.set_state(state_string, [3, 4, 0, 0])
        self.env.player = Pix.W
        self.env.opponent = Pix.B

        state, reward, is_done, info = self.env.step((0, 1, 1))

        self.assertEqual(reward, 10)
        self.assertEqual(list(self.env.mens), [2, 4, 0, 1])
        self.assertFalse(is_done)

    def test_killed_with_removed_piece(self):
        state_string = [
            # 123456789012
            'O-----O-----W',  # 0
            '| O---B---W |',  # 1
            '| | W-O-B | |',  # 2
            'B-O-O   W-O-W',  # 3
            '| | B-O-O | |',  # 4
            '| O---O---B |',  # 5
            'W-----O-----O',  # 6
        ]

        self.env.set_state(state_string, [3, 4, 0, 0])
        self.env.player = Pix.W
        self.env.opponent = Pix.B

        state, reward, is_done, info = self.env.step((0, 0, 2))

        self.assertEqual(reward, 10)
        self.assertEqual(list(self.env.mens), [2, 4, 0, 1])
        self.assertFalse(is_done)


if __name__ == '__main__':
    unittest.main()
