from __future__ import annotations
import math
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
        self.p = game.params.objects_manager.dragon
        self._health = 100

        self.action_mask = [None, [1, 1]]
        self.has_lost: bool = False

        self.body = Body()
        self.body.position = (
            random() * self.game.params.world.width,
            random() * self.game.params.world.height
        )
        self.shape = Circle(self.body, radius=self.p.size)
        self.shape.mass = self.p.initial_mass
        self.shape.friction = 0
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

    def get_health(self) -> float:
        return self._health

    def set_health(self, health: float) -> None:
        self._health = health

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

    def step(self):
        actions = self.policy(game=self.game)
        (x, y, r), a = actions

        # Force
        force = (x * self.p.force_max, y * self.p.force_max)
        self.body.apply_force_at_local_point(force=force, point=(0, 0))

        # Rotation
        rotation = self.p.rotation_max_speed * r
        self.body.angle -= rotation
        if self.body.torque != 0:
            print(self.body.torque)
        # print(self.body.rotation_vector)

    @staticmethod
    def get_angle(a, b, c):
        ang = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
        return abs(ang)
