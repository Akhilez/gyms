from typing import Tuple
from gym import Env
from gym.spaces import Discrete
import numpy as np
# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt


class SrYvlLvl0Env(Env):
    metadata = {'render.modes': ['human']}
    reward_range = (-np.inf, np.inf)

    # Set these in ALL subclasses
    action_space = Discrete(5)
    observation_space = Discrete(5)

    def __init__(
        self,
        world_size=50,
        max_agent_size=2,
        food_growth_density=2,
        food_growth_radius=5,
        initial_food_density=0.01,
        agent_growth_rate=0.01,
        shrink_rate_min=0.0005,
        shrink_rate_max=0.001,
        shrink_rate_idle=0.0001,

    ):
        super(SrYvlLvl0Env, self).__init__()
        self.agent_size = 1
        self.state = np.zeros((self.size, self.size))
        self.position = [0, 0]

        self.reset()

    def render(self, mode='human'):
        print(self.state)

    def step(self, action: int) -> Tuple[np.array, float, bool, bool, dict]:
        """
        0 = no action
        1 = left
        2 = up
        3 = right
        4 = down
        """
        self.state[self.position] = 0
        if action == 0:
            pass
        elif action == 1:
            self.position[1] = max(0, self.position[1] - 1)
        elif action == 2:
            self.position[0] = max(0, self.position[0] - 1)
        elif action == 3:
            self.position[1] = max(0, self.position[1] + 1)
        elif action == 4:
            self.position[0] = max(0, self.position[0] + 1)
        self.state[tuple(self.position)] = 1

        return self.state, reward, self.done, {}

    def reset(self, *_args, **_kwargs) -> None:
        self.state = np.zeros((self.size, self.size))
        self.position = [0, 0]

        self.state[tuple(self.position)] = 1


if __name__ == '__main__':
    env = SrYvlLvl0Env()
    env.reset()
    for i in range(10):
        env.render()
        env.step(3)
        env.render()
        env.step(4)
        env.render()
        env.step(1)
        env.render()
        env.step(2)
        env.render()




