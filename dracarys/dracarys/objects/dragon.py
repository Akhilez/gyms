from __future__ import annotations
from typing import TYPE_CHECKING

from arcade.examples.sprite_health import IndicatorBar

from dracarys.utils import get_distance
if TYPE_CHECKING:
    from dracarys.game import Game
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
        self.body.position = self._get_random_ground_position()
        self.shape = Circle(self.body, radius=self.p.size // 2)
        self.shape.mass = self.p.initial_mass
        self.shape.friction = 0
        self.shape.filter = self._walk_filter
        self.shape.parent = self
        self.game.world.space.add(self.body, self.shape)

        # Sprite
        image_source = "objects/images/dragon-1.png"
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
        image_source = "objects/images/Fire.png"
        self.fire_sprite = arcade.Sprite(
            image_source,
            scale=self.fire_size,
            angle=self.body.angle,
            center_x=self.body.position.x,
            center_y=self.body.position.y,
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.fire_sprite)

        self.health_bar: IndicatorBar = IndicatorBar(
            self,
            self.game.ui_manager.scene.get_sprite_list(SPRITE_LIST_DYNAMIC),
            (self.body.position.x, self.body.position.y),
        )

        # Key Stuff
        self.acquired_key = False
        self._key = None

    def draw(self):
        """Used to draw self onto arcade scene."""
        self.sprite.position = self.body.position
        self.sprite.radians = self.body.angle

        self.health_bar.position = (
            self.body.position.x,
            self.body.position.y
        )

        self.health_bar.background_box.radians = self.body.angle
        self.health_bar.full_box.radians = self.body.angle

        self.health_bar.angle = self.body.angle
        # Adjust Fire
        self.fire_sprite.position = self._fire_position
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
                if distance < self.fire_size * self.p.max_fire_radius * 2:
                    animal.burn()
            for crossbow in self.game.objects_manager.crossbows:
                distance = get_distance(self._fire_position, crossbow.center)
                if distance < self.fire_size * self.p.max_fire_radius * 2:
                    crossbow.burn()

        if a == DiscreteActions.ACT:
            self._fire_position = self._get_firing_position()

            # 1. If near a burnt animal, eats it.
            for animal in self.game.objects_manager.animals:
                if animal.burnt >= 1:
                    distance = get_distance(self._fire_position, animal.body.position)
                    if distance < self.p.eating_distance:
                        self.eat(animal)
                        return

            # 2. If near a gate and has key, unlocks it.
            if self.acquired_key:
                distance = get_distance(self._fire_position, self.game.world.gate.bb.center())
                if distance < self.p.eating_distance:
                    self.unlock()
                    return

            # 3. If near the key, hold it.
            if not self.game.objects_manager.unlocked_gate:
                for key in self.game.objects_manager.keys:
                    distance = get_distance(self._fire_position, key.body.position)
                    if distance < self.p.eating_distance:
                        self.hold_key(key)

        # If unlocked and outside the world, game over.
        if self.game.objects_manager.unlocked_gate and not self.game.episode_manager.ended and self._is_outside_the_world():
            self.game.episode_manager.ended = True

        self.health_bar.fullness = (
            1 - min(1, 1 - self.health)
        )

    def _get_firing_position(self):
        return self.body.local_to_world((0, 80 + self.fire_size * self.p.max_fire_radius * 3))

    def eat(self, animal):
        if not self.health > 0.9:
            self.health += self.p.health_regen_amount
        animal.health = 0

    def unlock(self):
        print("Unlocked gate")
        self.game.objects_manager.unlocked_gate = True
        self.shape.filter = ShapeFilter(mask=0)

    def hold_key(self, key):
        self.acquired_key = True
        self._key = key
        # Attach the key to the player
        key.acquired_by = self

    def on_collision(self, other: Shape):
        if other.filter.categories == CAT_ARROW:
            self.health -= self.p.health_decay_arrow
        elif other.filter.categories == CAT_WALL and self.game.objects_manager.unlocked_gate:
            # End game! You won!
            self.game.episode_manager.ended = True

    def _is_outside_the_world(self):
        x = self.body.position[0]
        y = self.body.position[1]

        return not 0 < x < self.game.params.world.width or not 0 < y < self.game.params.world.height
