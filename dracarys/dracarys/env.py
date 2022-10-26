from typing import Optional, Union, List, Mapping
import numpy as np
from gym import Env
from gym.core import RenderFrame, ActType
from gym.envs.registration import EnvSpec
from gym.spaces import Box
from dracarys.game import Game
from dracarys.params import Params
from dracarys.rules import ACTION_SPACE


P = Params.make('rl')


class SrYvl2(Env):
    metadata = {
        "render_modes": [
            "rgb_array",
            # "ansi",
        ]
    }
    reward_range = (0, 1)
    action_space = ACTION_SPACE
    observation_space = Box(low=0, high=255, shape=(3, P.ui.height, P.ui.width), dtype=np.uint8)
    spec = EnvSpec(
        id='sryvl2',
        entry_point='sryvl2.env:SrYvl2',
        max_episode_steps=10_000,
    )

    def __init__(self):
        self.game = Game(params=P)
        self.player = self.game.objects_manager.dragons[0]

    def reset(self, *_args, **_kwargs):
        self.__init__()
        return self.player.render()

    def step(self, action: ActType):
        self.player.policy = lambda **_: action
        done = self.player.has_lost
        observation = self.player.render()
        reward = self._find_reward()
        info = self._create_info()
        return observation, reward, done, done, info

    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        pass

    def _find_reward(self) -> float:
        return 0.0

    def _create_info(self) -> Mapping:
        return {}


def test_env():
    env = SrYvl2()
    for i in range(10):
        obs, _, _, _, _ = env.step(env.action_space.sample())
        print(obs.shape, obs.mean())


if __name__ == '__main__':
    test_env()
