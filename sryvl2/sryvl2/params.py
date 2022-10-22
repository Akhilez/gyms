from pydantic import BaseModel


class EpisodeParams(BaseModel):
    frames_per_timestep: int = 3
    total_timesteps: int = 10_000


class RulesParams(BaseModel):
    pass


class WorldParams(BaseModel):
    pass


class ObjectsManagerParams(BaseModel):
    pass


class StatsParams(BaseModel):
    pass


class UIParams(BaseModel):
    height: int = 224
    width: int = 224
    fps: float = 6


class Params(BaseModel):
    episode: EpisodeParams = EpisodeParams()
    rules: RulesParams = RulesParams()
    world: WorldParams = WorldParams()
    objects_manager: ObjectsManagerParams = ObjectsManagerParams()
    stats: StatsParams = StatsParams()
    ui: UIParams = UIParams()

    @staticmethod
    def make(mode='default'):
        if mode == 'default':
            return Params()
        if mode == 'human_single_player':
            return Params()
        if mode == 'rl':
            return Params()


def test_params():
    params = Params()
    print(params.episode.frames_per_timestep)


if __name__ == '__main__':
    test_params()

