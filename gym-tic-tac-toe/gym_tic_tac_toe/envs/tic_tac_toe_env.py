import gym
from gym import spaces
import numpy as np


class Pix:
    class X:
        string = 'X'
        tup = (0, 1, 0)
        arr = np.array(tup)

    class O:
        string = 'O'
        tup = (0, 0, 1)
        arr = np.array(tup)

    class S:
        string = '_'
        tup = (1, 0, 0)
        arr = np.array(tup)

    pix_to_str = {
        X.tup: X.string,
        O.tup: O.string,
        S.tup: S.string
    }
    str_to_tup = {
        X.string: X.tup,
        O.string: O.tup,
        S.string: S.tup
    }


Xs = Pix.X.string
Os = Pix.O.string
Ss = Pix.S.string

Xt = Pix.X.tup
Ot = Pix.O.tup
St = Pix.S.tup


class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(9)

        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=1, shape=(3, 3), dtype=np.uint8)

        self.player = Pix.O  # Current player
        self.rewards_for = Pix.X  # Which player is this reward for?

        self.state = None
        self.is_done = False
        self.count = 0

    def step(self, action: int):
        # return next_state, reward, is_done, info
        i = action // 3
        j = action % 3

        # Check if the action is LEGAL or not
        if any(self.state[i][j] != Pix.S.arr):
            # Exit
            return

        self.state[i][j] = self.player.arr
        self.count += 1
        self.is_done = self.count >= 9
        reward = 0

        won = self._who_won()

        if won is not None:
            self.is_done = True
            reward = 100 if won.string == self.rewards_for.string else -100

        return self.state, reward, self.is_done

    def reset(self):
        self.state = self._get_empty_state()
        self.is_done = False
        self.count = 0
        self.swap_players()
        return self.state

    def render(self, mode='human', close=False):
        string = []
        for r in range(3):
            for c in range(3):
                pixel = self.state[r, c, :]
                string.append(Pix.pix_to_str[tuple(pixel)])
            string.append('\n')
        state_str = ''.join(string)
        print(state_str)

    def set_state(self, state_str):
        self.state = []
        self.count = 0

        for row in state_str:
            state_row = []
            for pix in row:
                state_row.append(Pix.str_to_tup[pix])
                if pix != Pix.S.string:
                    self.count += 1
            self.state.append(state_row)

        self.state = np.array(self.state)
        self.is_done = self.count >= 9 or self._who_won() is not None

    def swap_players(self):
        self.player = Pix.O if self.player.string == Pix.X.string else Pix.X

    # ------- Private methods --------------

    @staticmethod
    def _get_empty_state():
        return np.zeros((3, 3, 3), dtype=np.uint8)

    def _who_won(self):
        pos_sum = np.array([
            # All rows
            self.state[0, :],
            self.state[1, :],
            self.state[2, :],

            # All columns
            self.state[:, 0],
            self.state[:, 1],
            self.state[:, 2],

            # Diagonals
            [self.state[0, 0], self.state[1, 1], self.state[2, 2]],
            [self.state[0, 2], self.state[1, 1], self.state[2, 0]]
        ]).sum(1)

        pos_argmax = pos_sum.argmax(1)
        win_conditions = np.logical_and((pos_sum.max(1) == 3), (pos_argmax > 0))

        won_indices = pos_argmax[win_conditions]

        if len(won_indices) > 0:
            return Pix.X if won_indices[0] == 1 else Pix.O
