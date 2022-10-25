from __future__ import annotations
from typing import TYPE_CHECKING
import arcade
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
            pymunk.Segment(self.space.static_body, (0, 0), (0, self.params.height), 1),
            pymunk.Segment(self.space.static_body, (0, self.params.height), (self.params.height, self.params.height), 1),
            pymunk.Segment(self.space.static_body, (self.params.height, self.params.height), (self.params.height, 0), 1),
            pymunk.Segment(self.space.static_body, (0, 0), (self.params.height, 0), 1),
        ]
        for s in self.boundaries:
            s.elasticity = .9
            s.friction = 0.0
        self.space.add(*self.boundaries)

        self.setup_boundaries()

    def step(self):
        self.space.step(dt=1.0 / self.game.params.ui.fps)

    def setup_boundaries(self):
        side = 128
        sprite = ":resources:images/tiles/dirtCenter.png"

        # Create bottom wall
        for x in range(0, self.params.height + side, side):
            wall = arcade.Sprite(
                sprite, 1,
                center_x=x,
                center_y=-side // 2,
                angle=270,
            )
            self.game.ui_manager.scene.add_sprite("Walls", wall)

        # Create left wall
        for x in range(0, self.params.height + side, side):
            wall = arcade.Sprite(
                sprite, 1,
                center_x=-side//2,
                center_y=x,
                angle=270,
            )
            self.game.ui_manager.scene.add_sprite("Walls", wall)

        # Create right wall
        for x in range(0, self.params.height + side, side):
            wall = arcade.Sprite(
                sprite, 1,
                center_x=self.params.width + side // 2,
                center_y=x,
                angle=90,
            )
            self.game.ui_manager.scene.add_sprite("Walls", wall)

        # Create top wall
        for x in range(0, self.params.width + side, side):
            wall = arcade.Sprite(
                sprite, 1,
                center_x=x,
                center_y=self.params.height + side // 2,
                angle=180,
            )
            self.game.ui_manager.scene.add_sprite("Walls", wall)
