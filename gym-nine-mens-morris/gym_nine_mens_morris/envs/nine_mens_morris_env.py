import gym
import numpy as np
from gym import spaces


class Pix:
    class S:
        string = 'O'
        tup = (1, 0, 0)
        arr = np.array(tup)

    class W:
        string = 'W'
        tup = (0, 1, 0)
        arr = np.array(tup)
        idx = np.array([0, 2])

    class B:
        string = 'B'
        tup = (0, 0, 1)
        arr = np.array(tup)
        idx = np.array([1, 3])

    tup_to_str = {
        S.tup: S.string,
        W.tup: W.string,
        B.tup: B.string
    }

    str_to_tup = {
        S.string: S.tup,
        W.string: W.tup,
        B.string: B.tup
    }


legal_moves = {

    # All corners
    (0, 0, 0): [None, None, (0, 1, 1), (0, 1, 0)],
    (0, 0, 1): [(0, 1, 1), None, None, (0, 1, 2)],
    (0, 0, 2): [(0, 1, 3), (0, 1, 2), None, None],
    (0, 0, 3): [None, (0, 1, 0), (0, 1, 3), None],

    (1, 0, 0): [None, None, (1, 1, 1), (1, 1, 0)],
    (1, 0, 1): [(1, 1, 1), None, None, (1, 1, 2)],
    (1, 0, 2): [(1, 1, 3), (1, 1, 2), None, None],
    (1, 0, 3): [None, (1, 1, 0), (1, 1, 3), None],

    (2, 0, 0): [None, None, (2, 1, 1), (2, 1, 0)],
    (2, 0, 1): [(2, 1, 1), None, None, (2, 1, 2)],
    (2, 0, 2): [(2, 1, 3), (2, 1, 2), None, None],
    (2, 0, 3): [None, (2, 1, 0), (2, 1, 3), None],

    # All edges
    (0, 1, 0): [None, (0, 0, 0), (1, 1, 0), (0, 0, 3)],
    (0, 1, 1): [(0, 1, 1), None, (0, 0, 1), (1, 0, 1)],
    (0, 1, 2): [(1, 1, 2), (0, 0, 1), None, (0, 0, 2)],
    (0, 1, 3): [(0, 0, 3), (1, 1, 3), (0, 0, 2), None],

    (1, 1, 0): [(0, 1, 0), (1, 0, 0), (2, 1, 0), (1, 0, 3)],
    (1, 1, 1): [(1, 1, 1), (0, 1, 1), (1, 0, 1), (2, 0, 1)],
    (1, 1, 2): [(2, 1, 2), (1, 0, 1), (0, 1, 2), (1, 0, 2)],
    (1, 1, 3): [(1, 0, 3), (2, 1, 3), (1, 0, 2), (0, 1, 3)],

    (2, 1, 0): [(1, 1, 0), (2, 0, 0), None, (2, 0, 3)],
    (2, 1, 1): [(2, 1, 1), (1, 1, 1), (2, 0, 1), None],
    (2, 1, 2): [None, (2, 0, 1), (1, 1, 2), (2, 0, 2)],
    (2, 1, 3): [(2, 0, 3), None, (2, 0, 2), (1, 1, 3)],

}


class NineMensMorrisEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Example when using discrete actions:
        self.action_space = spaces.MultiDiscrete((3, 2, 4, 4))

        # Example for using image as input:
        self.observation_space = spaces.Tuple((
            spaces.MultiDiscrete([3, 2, 4, 3]),
            spaces.MultiDiscrete([4, 9])
        ))

        self.board = None
        self.mens = None
        self.is_done = False  # True when episode is complete
        self.player = Pix.W
        self.opponent = Pix.B

    def step(self, position, move=None, kill_location=None):
        """
        :param position: a 3,2,4 tuple
        :param move: a scalar
        :param kill_location: position tuple where the opponent's piece is removed.
        :return: state, reward, is_done, info
        """

        unused, killed = self.mens[self.player.idx]
        moved_position = self._get_moved_position(position, move)
        is_phase_1 = unused > 0
        is_illegal = self._is_action_illegal(position, moved_position, is_phase_1)
        if is_illegal:
            return self.board, -100, self.is_done, is_illegal

        if is_phase_1:
            self.board[position] = self.player.arr
            target_position = position
            self.mens[self.player.idx][0] -= 1  # Unused will be reduced by 1
        else:
            self.board[position] = Pix.S.arr
            self.board[moved_position] = self.player.arr
            target_position = moved_position

        reward = 0

        has_killed = self._has_killed(target_position)
        if has_killed:
            reward = 10
            if kill_location is not None and self.board[kill_location] == self.opponent.arr:
                self.board[kill_location] = Pix.S.arr
                self.mens[self.opponent.idx][1] += 1
            else:
                return self.board, reward, self.is_done, "Invalid kill_location"

        self.is_done = self._is_done()
        if self.is_done:
            reward = 100

        self.swap_players()

        return self.board, reward, self.is_done, None

    def reset(self):
        self.board, self.mens = self._get_empty_state()
        self.is_done = False

        return self.board

    def render(self, mode='human', close=False):
        s = [
            (0, 0, 0), (0, 1, 1), (0, 0, 1),
            (1, 0, 0), (1, 1, 1), (1, 0, 1),
            (2, 0, 0), (2, 1, 1), (2, 0, 1),
            (0, 1, 0), (1, 1, 0), (2, 1, 0), (0, 1, 2), (1, 1, 2), (2, 1, 2),
            (2, 0, 3), (2, 1, 3), (2, 0, 3),
            (1, 0, 3), (1, 1, 3), (1, 0, 2),
            (0, 0, 3), (0, 1, 3), (0, 0, 2),
        ]
        s = [Pix.tup_to_str[tuple(self.board[x])] for x in s]
        string = f"""
{s[0]}-----{s[1]}-----{s[2]}
| {s[3]}---{s[4]}---{s[5]} |
| | {s[6]}-{s[7]}-{s[8]} | |
{s[9]}-{s[10]}-{s[11]}   {s[12]}-{s[13]}-{s[14]}
| | {s[15]}-{s[16]}-{s[17]} | |
| {s[18]}---{s[19]}---{s[20]} |
{s[21]}-----{s[22]}-----{s[23]}
        """
        print(f"Current Player: {self.player.string}")
        print(self.mens)
        print(string)

    def swap_players(self):
        opponent = self.opponent
        self.opponent = self.player
        self.player = opponent

    def set_state(self, board_str, mens):
        self.reset()

        s = board_str

        self.board = np.array([
            # Outer layer
            [
                [Pix.str_to_tup[s[0][0]], Pix.str_to_tup[s[0][12]], Pix.str_to_tup[s[6][-1]], Pix.str_to_tup[s[6][0]]],
                [Pix.str_to_tup[s[3][0]], Pix.str_to_tup[s[0][6]], Pix.str_to_tup[s[3][-1]], Pix.str_to_tup[s[-1][6]]],
            ],

            # Middle layer
            [
                [Pix.str_to_tup[s[1][2]], Pix.str_to_tup[s[1][10]], Pix.str_to_tup[s[5][10]], Pix.str_to_tup[s[5][2]]],
                [Pix.str_to_tup[s[2][3]], Pix.str_to_tup[s[1][6]], Pix.str_to_tup[s[3][10]], Pix.str_to_tup[s[5][6]]],
            ],

            # Inner layer
            [
                [Pix.str_to_tup[s[2][4]], Pix.str_to_tup[s[4][8]], Pix.str_to_tup[s[4][8]], Pix.str_to_tup[s[4][4]]],
                [Pix.str_to_tup[s[4][3]], Pix.str_to_tup[s[2][6]], Pix.str_to_tup[s[3][8]], Pix.str_to_tup[s[4][6]]],
            ],
        ])

        self.mens = mens
        self.is_done = self._is_done()

    # ----- Private Methods ------

    def _is_action_illegal(self, position, moved_position, is_phase_1):
        """
        Phase 1:
          - Position not empty
        Phase 2:
          - Position is non-player
          - Move is none
          - Moved position is out of bounds
          - Moved position is not empty
        """

        if is_phase_1:
            if all(self.board[position] != Pix.S.tup):
                return "During phase 1, the position must be empty."
        else:  # Phase 2
            if self.board[position] != self.player.tup:
                return "During phase 2, the position must be player's piece"
            if moved_position is None:  # Out of bounds
                return "Can't move the piece to that position."
            if self.board[moved_position] != Pix.S.tup:  # Is not empty
                return "The moved position must be empty."

        return False

    def _has_killed(self, recent_move):
        # Check all 4 edges of recently moved position.
        # If there's a 3 in a line, then remove desired piece.

        left, up, right, down = legal_moves[recent_move]

        if left is not None and right is not None:
            if self.board[left] == self.board[recent_move] and self.board[right] == self.board[recent_move]:
                return True
        if up is not None and down is not None:
            if self.board[up] == self.board[recent_move] and self.board[down] == self.board[recent_move]:
                return True

    def _is_done(self):
        return self.mens[2] == 9 or self.mens[3] == 9

    @staticmethod
    def _get_moved_position(position, move):
        """
        :param position: array of shape (3, 2, 4) -> position on the board.
        :param move: one of [0, 1, 2, 3]
        :return: position of the move.
        """

        if move is None:
            return

        return legal_moves[position][move]

    @staticmethod
    def _get_empty_state():
        board = np.zeros((3, 2, 4, 3), dtype=np.uint8)
        board[:, :, :, 0] = 1

        mens = np.array([8, 8, 0, 0])

        return board, mens
