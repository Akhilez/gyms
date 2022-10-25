from __future__ import annotations
from typing import TYPE_CHECKING

import pymunk
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
        self.space.damping = self.params.damping

        self.boundaries = [
            pymunk.Segment(self.space.static_body, (50, 50), (50, self.params.height - 50), 5),
            pymunk.Segment(self.space.static_body, (50, self.params.height - 50), (self.params.height - 50, self.params.height - 50), 5),
            pymunk.Segment(self.space.static_body, (self.params.height - 50, self.params.height - 50), (self.params.height - 50, 50), 5),
            pymunk.Segment(self.space.static_body, (50, 50), (self.params.height - 50, 50), 5),
        ]
        for s in self.boundaries:
            s.elasticity = .9
            s.friction = 0.1
        self.space.add(*self.boundaries)

    def step(self):
        self.space.step(dt=1.0 / self.game.params.ui.fps)
