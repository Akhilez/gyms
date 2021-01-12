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

    def test_renders_without_errors(self):
        self.env.reset()
        self.env.render()

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

        self.env.step(((0, 0, 0), None, None))
        player_2 = self.env.player.string

        self.assertNotEqual(player_1, player_2)

    def test_not_done(self):
        self.env.reset()

        _, _, is_done, _ = self.env.step(((0, 0, 0), None, None))

        self.assertFalse(is_done)

        self.env.mens = np.array([0, 0, 0, 8])
        self.assertFalse(self.env.is_done)

    def test_done(self):
        self.env.reset()

        self.env.mens = np.array([0, 0, 8, 9])

        _, _, is_done, _ = self.env.step((0, 0, 0))

        self.assertTrue(is_done)

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

        state, reward, is_done, info = self.env.step(((0, 1, 1), None, None))

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
        old_board = np.array(self.env.board)

        (state, _), reward, is_done, info = self.env.step(((0, 1, 1), None, None))

        self.assertIsNotNone(info)
        self.assertEqual(reward, 0)
        self.assertEqual(list(self.env.mens), [3, 4, 0, 0])
        self.assertFalse(is_done)
        np.testing.assert_array_equal(old_board, state)

        (state, _), reward, is_done, info = self.env.step(((0, 1, 1), None, (0, 1, 2)))

        self.assertEqual(reward, 0)
        self.assertEqual(list(self.env.mens), [3, 4, 0, 0])
        self.assertFalse(is_done)
        np.testing.assert_array_equal(old_board, state)

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

        (state, _), reward, is_done, info = self.env.step(((0, 0, 2), None, (1, 1, 1)))

        self.assertEqual(reward, 10)
        self.assertEqual(list(self.env.mens), [2, 4, 0, 1])
        self.assertFalse(is_done)
        np.testing.assert_array_equal(state[1, 1, 1], Pix.S.arr)

    def test_illegal_move_overlap(self):
        self.env.reset()
        self.env.player = Pix.W
        (state, _), *_ = self.env.step(((0, 0, 0), None, None))
        np.testing.assert_array_equal(state[0, 0, 0], Pix.W.arr)
        (state, _), _, _, info = self.env.step(((0, 0, 0), None, None))

        np.testing.assert_array_equal(state[0, 0, 0], Pix.W.arr)
        self.assertIsNotNone(info)
        self.assertEqual(self.env.player, Pix.B)

    def test_illegal_move_phase_2(self):
        self.env.reset()
        self.env.player = Pix.W
        self.env.step(((0, 0, 0), None, None))
        self.env.mens = np.zeros(4)

        (state, _), _, _, info = self.env.step(((0, 0, 0), None, None))  # B
        np.testing.assert_array_equal(state[0, 0, 0], Pix.W.arr)
        self.assertIsNotNone(info)
        self.assertEqual(self.env.player, Pix.B)

        # Move to out of bounds
        self.player = Pix.W
        (state, _), _, _, info = self.env.step(((0, 0, 0), 0, None))  # W
        self.assertIsNotNone(info)

        # Moved position is not empty
        self.player = Pix.B
        self.env.mens = np.array([8, 8, 0, 0])
        _, _, _, info = self.env.step(((0, 1, 1), None, None))  # B
        (state, _), _, _, info = self.env.step(((0, 0, 0), 2, None))  # W
        self.assertIsNotNone(info)
        np.testing.assert_array_equal(state[0, 0, 0], Pix.W.arr)
        np.testing.assert_array_equal(state[0, 1, 1], Pix.B.arr)

    def test_legal_actions_phase_1(self):
        self.env.reset()
        self.env.step(((0, 0, 0), None, None))
        self.env.step(((0, 0, 1), None, None))
        actions = self.env.get_legal_actions()

        self.assertEqual(len(actions), 22)

    def test_legal_actions_phase_2_no_kill(self):
        self.env.reset()
        self.env.step(((0, 0, 0), None, None))
        self.env.step(((0, 0, 1), None, None))
        self.env.mens = np.zeros(4)
        actions = self.env.get_legal_actions()

        self.assertEqual(len(actions), 2)

    def test_legal_actions_phase_1_kill(self):
        self.env.reset()
        self.env.step(((0, 0, 0), None, None))
        self.env.step(((0, 0, 1), None, None))
        self.env.step(((0, 0, 3), None, None))
        self.env.step(((0, 1, 3), None, None))
        actions = self.env.get_legal_actions()

        self.assertEqual(len(actions), 21)


if __name__ == '__main__':
    unittest.main()
