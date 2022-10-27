from __future__ import annotations
from abc import abstractmethod, ABC
from random import random
from typing import TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    from dracarys.game import Game


class Character(ABC):
    def __init__(self, game: Game):
        self.game = game
        self.health = 5.0
        self.action_space = None

        self.body = None
        self.shape = None
        self.sprite = None

    def policy(self, **_kwargs):
        return self.action_space.sample()

    def render(self) -> np.array:
        """Used to get a view of the world from the character's perspective."""
        return self.game.ui_manager.render_for(self)

    @abstractmethod
    def draw(self):
        """Used to draw self onto arcade scene."""
        pass

    def step(self):
        pass

    def _get_random_ground_position(self):
        x, y = (
            random() * self.game.params.world.width,
            random() * self.game.params.world.height
        )

        xr = self.body.position[0] // self.game.params.world.cell_size
        yr = self.body.position[1] // self.game.params.world.cell_size

        if (xr, yr) in zip(*self.game.world.hill_indices):
            return self._get_random_ground_position()
        return x, y

