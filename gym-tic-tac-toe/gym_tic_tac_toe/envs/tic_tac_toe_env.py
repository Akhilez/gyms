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

        self.state = None
        self.is_done = False

    def step(self, action: int):
        # return next_state, reward, is_done, info
        i = 9 // action
        j = 9 % action

        # Check if the action is LEGAL or not
        if self.state[i][j] == Pix.S.arr:
            prev_state = np.copy(self.state)
            self.state[i][j] = Pix.X.arr

        return 1

    def reset(self):
        self.state = self._get_empty_state()
        self.is_done = False
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
        state = np.array([[Pix.str_to_tup[pix] for pix in row] for row in state_str])
        self.state = state

    # ------- Private methods --------------

    @staticmethod
    def _get_empty_state():
        return np.zeros((3, 3, 3), dtype=np.uint8)
