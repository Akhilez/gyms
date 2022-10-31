from typing import Mapping
import numpy as np
from PIL import Image
from gym import Env
from gym.envs.registration import EnvSpec
from gym.spaces import Box
from dracarys.constants import DISCRETE_ACTION_SPACE, DiscreteActions
from dracarys.game import Game
from dracarys.params import Params


P = Params.make('rl')

FORCE = 1
ROTATION = 1


def discrete_actions_to_continuos(action):
    x, y, r, a = 0.0, 0.0, 0.0, 0
    if action == DiscreteActions.UP:# self.up_pressed:
        y += FORCE
    if action == DiscreteActions.DOWN:# self.down_pressed:
        y -= FORCE
    if action == DiscreteActions.LEFT:# self.left_pressed:
        x -= FORCE
    if action == DiscreteActions.RIGHT:# self.right_pressed:
        x += FORCE
    if action == DiscreteActions.TURN_LEFT:# self.turn_left:
        r -= ROTATION
    if action == DiscreteActions.TURN_RIGHT:# self.turn_right:
        r += ROTATION
    if action == DiscreteActions.FIRE:# self.fire_pressed:
        a = DiscreteActions.FIRE
    if action == DiscreteActions.ACT:# self.act_pressed:
        a = DiscreteActions.ACT

    return (x, y, r), a


class DracarysEnv(Env):
    metadata = {
        "render_modes": [
            "rgb_array",
            # "ansi",
        ]
    }
    reward_range = (0, 1)
    action_space = DISCRETE_ACTION_SPACE
    observation_space = Box(low=0, high=255, shape=(128, 128, 3), dtype=np.uint8)
    spec = EnvSpec(
        id='dracarys-v1',
        entry_point='dracarys.env:DracarysEnv',
        max_episode_steps=10_000,
    )

    def __init__(self):
        self.game = Game(params=P)
        self.player = self.game.objects_manager.dragons[0]
        self.previous_health = self.player.health

    def reset(self, *_args, **_kwargs):
        self.__init__()
        return self.render()

    def step(self, action):
        self.player.policy = lambda **_: discrete_actions_to_continuos(action)
        for i in range(self.game.params.episode.frames_per_timestep):
            self.game.step()
        done = self.game.episode_manager.ended
        observation = self.render()
        reward = self.player.stats.get_reward()
        info = self._create_info()
        return observation, reward, done, info

    def render(self):
        img = self.player.render()
        img = Image.fromarray(img).resize((128, 128))
        img = np.asarray(img)
        return img

    def _create_info(self) -> Mapping:
        return {}


def _test_env():
    from PIL import Image
    env = DracarysEnv()
    for i in range(5):
        action = discrete_actions_to_continuos(env.action_space.sample())
        print(action)
        obs, _, _, _ = env.step(action)
        Image.fromarray(obs).show()


if __name__ == '__main__':
    _test_env()
