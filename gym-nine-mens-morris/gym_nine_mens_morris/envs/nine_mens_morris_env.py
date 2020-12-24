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
        self.action_space = spaces.Discrete(9)

        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=255, shape=
            (HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)
        pass

    def step(self, action):
        # return next_state, reward, is_done, info
        return 1

    def reset(self):
        return 0

    def render(self, mode='human', close=False):
        print("hello")
