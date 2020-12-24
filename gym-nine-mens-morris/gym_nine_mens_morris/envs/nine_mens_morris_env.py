import gym
import numpy as np
from gym import spaces


class Pix:
    class S:
        string = '_'
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


class NineMensMorrisEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Example when using discrete actions:
        self.action_space = spaces.MultiDiscrete((3 * 3 * 3, 4))

        # Example for using image as input:
        self.observation_space = spaces.Tuple((
            spaces.Box(low=0, high=1, shape=(3, 3, 3, 3), dtype=np.uint8),
            spaces.MultiDiscrete([4, 9])
        ))

        self.board = None
        self.mens = None
        self.is_done = False  # True when episode is complete
        self.player = None

    def step(self, position, move=None):
        # return next_state, reward, is_done, info

        is_illegal = self._is_action_illegal(position, move)
        if is_illegal:
            return None, None, None, is_illegal

        return self.board, 0, self.is_done, None

    def reset(self):
        self.board, self.mens = self._get_empty_state()
        self.is_done = False

        return self.board

    def render(self, mode='human', close=False):
        print("hello")

    # ----- Private Methods ------

    def _is_action_illegal(self, position, move):
        """
        Legal action or not
            if position is not empty, then illegal
            if pieces are used and move is given and it is not empty, then illegal
            # if pieces are unused and move is given, then illegal
            if move is given and move is out of bounds, then illegal
            if pieces are used and move is not given, then illegal
        """
        position = np.unravel_index(position, (3, 3, 3))
        unused, killed = self.mens[self.player.idx]

        if self.board[position] != Pix.S.arr:
            return True


        if move is not None:
            move = self._unravel_move(position, move)

            if unused == 0:
                pass
        # Move's position is out of bounds

        else:
            if unused == 0:
                return True

    @staticmethod
    def _unravel_move(position, move):
        """
        :param position: array of shape (3, 3, 3) -> position on the board.
        :param move: array of shape (2) -> unused and killed
        :return: position of the move.
        """
        pass


    @staticmethod
    def _get_empty_state():
        board = np.zeros((3 * 3 * 3, 3), dtype=np.uint8)
        board[:, 0] = 1
        board = board.reshape((3, 3, 3, 3))

        mens = np.array([8, 8, 0, 0])

        return board, mens
