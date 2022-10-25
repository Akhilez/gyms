from __future__ import annotations
from random import random
from typing import TYPE_CHECKING

import arcade
import numpy as np
from pymunk import Body, Circle
if TYPE_CHECKING:
    from dracarys.game import Game
from dracarys.rules import ACTION_SPACE


class Character:
    def __init__(self, game: Game):
        self.game = game
        self.p = game.params.objects_manager.character

        self.action_mask = [None, [1, 1]]
        self.has_lost: bool = False

        self.body = Body()
        self.body.position = (
            # random() * self.game.params.world.width,
            # random() * self.game.params.world.height
            100, 200
        )
        self.shape = Circle(self.body, radius=self.p.size)
        self.shape.mass = self.p.initial_mass
        self.shape.friction = 1
        self.game.world.space.add(self.body, self.shape)

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/space_shooter/playerShip3_orange.png"
        self.player_sprite = arcade.Sprite(
            image_source,
            scale=40 / 128,
            angle=self.body.angle,
            center_x=self.body.position.x,
            center_y=self.body.position.y,
        )
        self.game.ui_manager.scene.add_sprite("Player", self.player_sprite)

    def policy(self, **_kwargs):
        # TODO: Sample only legal actions
        return ACTION_SPACE.sample()

    def render(self) -> np.array:
        """Used to get a view of the world from the character's perspective."""
        return self.game.ui_manager.render_for(self)

    def draw(self):
        """Used to draw self onto arcade scene."""
        arcade.draw_circle_filled(
            center_x=self.body.position.x,
            center_y=self.body.position.y,
            radius=self.shape.radius,
            color=arcade.color.RED,
        )
        self.player_sprite.position = self.body.position
        self.player_sprite.radians = self.body.angle
