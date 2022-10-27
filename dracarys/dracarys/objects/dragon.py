from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dracarys.game import Game
from random import random
import arcade
from pymunk import ShapeFilter, Body, Circle
from dracarys.constants import (
    CAT_DRAGON_WALK, CAT_DRAGON_FLY, CAT_ROCK, CAT_ANIMAL, DRAGON_ACTION_SPACE, DiscreteActions
)
from dracarys.objects.character import Character
from dracarys.constants import SPRITE_LIST_DYNAMIC


class Dragon(Character):
    def __init__(self, game: Game):
        super(Dragon, self).__init__(game)
        self.p = game.params.objects_manager.dragon
        self.action_space = DRAGON_ACTION_SPACE
        self.fire_size = 0.0  # (0-1)

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
            random() * self.game.params.world.width,
            random() * self.game.params.world.height
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
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.sprite)

        # Fire Sprite
        self._fire_position = self.body.position
        image_source = ":resources:images/tiles/torch1.png"
        self.fire_sprite = arcade.Sprite(
            image_source,
            scale=self.fire_size,
            angle=self.body.angle,
            center_x=self.body.position.x,
            center_y=self.body.position.y,
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.fire_sprite)

    def draw(self):
        """Used to draw self onto arcade scene."""
        self.sprite.position = self.body.position
        self.sprite.radians = self.body.angle

        # Adjust Fire
        self.fire_sprite.position = self.body.position
        self.fire_sprite.radians = self.body.angle
        self.fire_sprite.scale = self.fire_size

    def step(self):
        actions = self.policy(game=self.game)
        (x, y, r), a = actions

        # Force
        force = (x * self.p.force_max, y * self.p.force_max)
        self.body.apply_force_at_local_point(force=force, point=(0, 0))

        # Rotation
        rotation = self.p.rotation_max_speed * r
        self.body.angle -= rotation

        if a != DiscreteActions.FIRE:
            self.fire_size = 0
        else:
            self.fire_size = min(1, self.fire_size + self.p.fire_growth_rate)
            self._fire_position = self._get_firing_position()
            # objects_fired = self.game.world.space.point_query(
            #     self._fire_position,
            #     max_distance=self.fire_size * self.p.max_fire_size,
            #     shape_filter=ShapeFilter(categories=CAT_ANIMAL)
            # )
            # objects_fired = [s for s in objects_fired if s.shape.filter.categories == CAT_ANIMAL]
            for animal in self.game.objects_manager.animals:
                distance = self.get_distance(self._fire_position, animal.body.position)
                if distance < self.fire_size * self.p.max_fire_size:
                    animal.burn()

        if a == DiscreteActions.ACT:
            # 1. If near a burnt animal, eats it.
            self._fire_position = self._get_firing_position()
            for animal in self.game.objects_manager.animals:
                if animal.burnt >= 1:
                    distance = self.get_distance(self._fire_position, animal.body.position)
                    if distance < self.p.eating_distance:
                        self.eat(animal)

            # 2. If near the key, holds it.
            # 3. If near a gate and has key, unlocks it.

    def _get_firing_position(self):
        # TODO: Get the firing position
        return self.body.position

    def eat(self, animal):
        self.health += self.p.health_regen_amount
        animal.health = 0

    @staticmethod
    def get_angle(a, b, c):
        ang = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
        return abs(ang)

    @staticmethod
    def get_distance(a, b):
        distance = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
        return distance
