from gym import Env


class SrYvl(Env):
    def __init__(self):
        super(SrYvl, self).__init__()
        self.params_injector = ParameterInjector.get_instance()
        self.episode_manager = EpisodeManager(self)
        self.population_manager = PopulationManager(self)
        self.stats = Stats(self)
        self.ui_manager = UIManager(self)

    def step(self, action):


    def reset(self):
        pass

    def render(self, mode="human"):
        pass

