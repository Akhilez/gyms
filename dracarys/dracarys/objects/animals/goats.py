from __future__ import annotations
import arcade
from random import randrange, random
from pymunk import ShapeFilter, Body, Circle
from dracarys.constants import CAT_ANIMAL
from typing import TYPE_CHECKING

from dracarys.objects.character import Character

if TYPE_CHECKING:
    from dracarys.game import Game


class Goats(Character):
    def __init__(self, game: Game):
        super(Goats, self).__init__(game)
        self.p = game.params.objects_manager.animal
        self.x = randrange(500)
        self.y = randrange(500)

        # Collision Filters
        self._walk_filter = ShapeFilter(categories=CAT_ANIMAL)

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
        image_source = "objects/images/goat.png"
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
