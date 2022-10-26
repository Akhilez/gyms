import math

from pydantic import BaseModel


class EpisodeParams(BaseModel):
    frames_per_timestep: int = 3
    total_timesteps: int = 10_000


class RulesParams(BaseModel):
    pass


class WorldParams(BaseModel):
    height: int = 1024  # Multiple of 32
    width: int = 1024  # Multiple of 32
    damping: float = 0.5


class CharacterParams(BaseModel):
    initial_mass: float = 1
    size: float = 64


class DragonParams(CharacterParams):
    rotation_max_speed: float = math.pi / 32
    force_max: float = 500.0


class AnimalParams(CharacterParams):
    size: float = 10
    rotation_max_speed: float = math.pi / 128
    force_max: float = 100


class ObjectsManagerParams(BaseModel):
    dragon: DragonParams = DragonParams()
    animal: AnimalParams = AnimalParams()


class StatsParams(BaseModel):
    pass


class UIParams(BaseModel):
    height: int = 500
    width: int = 500
    fps: float = 30


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
