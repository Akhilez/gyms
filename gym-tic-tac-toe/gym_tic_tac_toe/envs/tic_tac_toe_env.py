import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(9)

        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=1, shape=(3, 3), dtype=np.uint8)

    def step(self, action):
        # return next_state, reward, is_done, info
        return 1

    def reset(self):
        return 0

    def render(self, mode='human', close=False):
        print("hello")
