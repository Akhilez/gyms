from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sryvl2.game import Game


class World:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.world

        """
        Create a world. Only positions, no real matrix.
        Set boundaries with pymunk static bodies.
        Create terrain with pymunk static bodies.
        
        """

    def step(self):
        pass
