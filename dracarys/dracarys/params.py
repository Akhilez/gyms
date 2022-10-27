import math
from pydantic import BaseModel


class EpisodeParams(BaseModel):
    frames_per_timestep: int = 3
    total_timesteps: int = 10_000


class WorldParams(BaseModel):
    height: int = 1024  # Multiple of 32
    width: int = 1024  # Multiple of 32
    damping: float = 0.5
    n_towers: int = 3
    cell_size: int = 8
    tower_size: int = 40


class CharacterParams(BaseModel):
    initial_mass: float = 1
    size: float = 64


class CrossBowParams(CharacterParams):
    size: float = 35
    observable_distance: float = 500
    shoot_probability: float = 1 / (60 * 2)
    burn_amount: float = 1e-2
    min_reload_time: int = 60  # 1 second


class ArrowParams(CharacterParams):
    size: float = 28
    initial_mass: float = 0.1
    impulse: float = 30


class DragonParams(CharacterParams):
    rotation_max_speed: float = math.pi / 32
    force_max: float = 500.0
    max_fire_radius: float = 16
    fire_growth_rate: float = 0.1
    eating_distance: float = 64
    health_regen_amount: float = 0.1
    health_decay: float = 0.0005
    health_decay_arrow: float = 0.05


class AnimalParams(CharacterParams):
    size: float = 25
    rotation_max_speed: float = math.pi / 32
    force_max: float = 10
    health_decay_rate: float = 1e-3
    burn_amount: float = 5e-2


class ObjectsManagerParams(BaseModel):
    dragon: DragonParams = DragonParams()
    animal: AnimalParams = AnimalParams()
    crossbow: CrossBowParams = CrossBowParams()
    arrow: ArrowParams = ArrowParams()
    n_animals: int = 10


class StatsParams(BaseModel):
    pass


class UIParams(BaseModel):
    height: int = 500
    width: int = 500
    fps: float = 30


class Params(BaseModel):
    episode: EpisodeParams = EpisodeParams()
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
