from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dracarys.game import Game
from random import random
import arcade
from pymunk import ShapeFilter, Body, Circle
from dracarys.constants import CAT_DRAGON_WALK, CAT_DRAGON_FLY, CAT_ROCK, CAT_ANIMAL
from dracarys.objects.character import Character
from dracarys.rules import ACTION_SPACE


class Dragon(Character):
    def __init__(self, game: Game):
        super(Dragon, self).__init__(game)
        self.p = game.params.objects_manager.dragon
        self.action_space = ACTION_SPACE
        self.power = 5
        self.drag_level = 0

        # Collision Filters
        self._walk_filter = ShapeFilter(categories=CAT_DRAGON_WALK)
        self._fly_filter = ShapeFilter(
            categories=CAT_DRAGON_FLY,
            # When flying, collides with all except rocks & animals
            mask=ShapeFilter.ALL_MASKS() ^ (CAT_ROCK | CAT_ANIMAL)
        )

        # Setup PyMunk body and shape
        self.body = Body()
        self.body.position = (
            self.game.params.world.width // 2,
            self.game.params.world.height // 2,
            # random() * self.game.params.world.width,
            # random() * self.game.params.world.height
        )
        self.shape = Circle(self.body, radius=self.p.size // 3)
        self.shape.mass = self.p.initial_mass
        self.shape.friction = 0
        self.shape.filter = self._walk_filter
        self.game.world.space.add(self.body, self.shape)

        # Sprite
        image_source = "objects/images/dragon-1-without-flame.png"
        self.sprite = arcade.Sprite(
            image_source,
            scale=self.p.size / 128,
            angle=self.body.angle,
            center_x=self.body.position.x,
            center_y=self.body.position.y,
        )
        self.game.ui_manager.scene.add_sprite("Player", self.sprite)

    def draw(self):
        """Used to draw self onto arcade scene."""
        self.sprite.position = self.body.position
        self.sprite.radians = self.body.angle

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
