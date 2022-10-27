from __future__ import annotations
from typing import TYPE_CHECKING
from dracarys.utils import get_distance
if TYPE_CHECKING:
    from dracarys.game import Game
from random import random
import arcade
from pymunk import ShapeFilter, Body, Circle, Shape
from dracarys.constants import (
    CAT_DRAGON_WALK, CAT_DRAGON_FLY, CAT_ROCK, CAT_ANIMAL, DRAGON_ACTION_SPACE, DiscreteActions, CAT_TOWER, CAT_ARROW,
    CAT_WALL
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
            mask=ShapeFilter.ALL_MASKS() ^ (CAT_ROCK | CAT_TOWER | CAT_ANIMAL)
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
        self.shape.parent = self
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
        self.health -= self.p.health_decay

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
            for animal in self.game.objects_manager.animals:
                distance = get_distance(self._fire_position, animal.body.position)
                if distance < self.fire_size * self.p.max_fire_size:
                    animal.burn()
            for crossbow in self.game.objects_manager.crossbows:
                distance = get_distance(self._fire_position, crossbow.center)
                if distance < self.fire_size * self.p.max_fire_size * 2:
                    crossbow.burn()

        if a == DiscreteActions.ACT:
            # 1. If near a burnt animal, eats it.
            self._fire_position = self._get_firing_position()
            for animal in self.game.objects_manager.animals:
                if animal.burnt >= 1:
                    distance = get_distance(self._fire_position, animal.body.position)
                    if distance < self.p.eating_distance:
                        self.eat(animal)

            # TODO: 2. If near the key, holds it.
            # TODO: 3. If near a gate and has key, unlocks it.

    def _get_firing_position(self):
        # TODO: Get the firing position
        return self.body.position

    def eat(self, animal):
        self.health += self.p.health_regen_amount
        animal.health = 0

    def on_collision(self, other: Shape):
        if other.filter.categories == CAT_ARROW:
            self.health -= self.p.health_decay_arrow
        elif other.filter.categories == CAT_WALL and self.game.objects_manager.unlocked_gate:
            # End game! You won!
            pass
