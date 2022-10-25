from __future__ import annotations
from typing import TYPE_CHECKING
from pymunk import Space
if TYPE_CHECKING:
    from dracarys.game import Game


class World:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.world

        """
        Create a world. Only positions, no real matrix.
        Set boundaries with pymunk static bodies.
        Create terrain with pymunk static bodies.
        
        """

        self.space = Space()

    def step(self):
        self.space.step(dt=1.0 / self.game.params.ui.fps)
