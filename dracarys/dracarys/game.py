from typing import Union
from dracarys.episode_manager import EpisodeManager
from dracarys.objects_manager import ObjectsManager
from dracarys.params import Params
from dracarys.ui_manager import UIManager
from dracarys.world import World


class Game:
    def __init__(self, params: Union[str, Params] = 'default'):
        self.params = Params.make(params) if type(params) is str else params
        self.episode_manager = EpisodeManager(self)
        self.ui_manager = UIManager(self)
        self.world = World(self)
        self.objects_manager = ObjectsManager(self)

    def step(self):
        self.episode_manager.step()
        self.objects_manager.step()
        self.world.step()
        self.ui_manager.step()
