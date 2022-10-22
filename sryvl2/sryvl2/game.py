from sryvl2.episode_manager import EpisodeManager
from sryvl2.objects_manager import ObjectsManager
from sryvl2.params import Params
from sryvl2.rules import Rules
from sryvl2.stats import Stats
from sryvl2.ui_manager import UIManager
from sryvl2.world import World


class Game:
    def __init__(self, mode='default'):
        self.params = Params.make(mode)
        self.episode_manager = EpisodeManager(self)
        self.rules = Rules(self)
        self.world = World(self)
        self.objects_manager = ObjectsManager(self)
        self.stats = Stats(self)
        self.ui_manager = UIManager(self)

    def step(self):
        self.episode_manager.step()
        self.objects_manager.step()
        self.world.step()
        self.stats.step()
        self.ui_manager.step()
