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

    class B:
        string = 'B'
        tup = (0, 0, 1)
        arr = np.array(tup)


class NineMensMorrisEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Example when using discrete actions:
        self.action_space = spaces.MultiDiscrete((9, 4))

        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=1, shape=(3, 3, 3, 3), dtype=np.uint8)

        self.state = None

        self.is_done = False  # True when episode is complete

    def step(self, action):
        # return next_state, reward, is_done, info
        return 1

    def reset(self):
        self.state = self._get_empty_state()
        self.is_done = False

        return self.state

    def render(self, mode='human', close=False):
        print("hello")

    # ----- Private Methods ------

    @staticmethod
    def _get_empty_state():
        state = np.zeros((3 * 3 * 3, 3), dtype=np.uint8)
        state[:, 0] = 1
        return state.reshape((3, 3, 3, 3))
