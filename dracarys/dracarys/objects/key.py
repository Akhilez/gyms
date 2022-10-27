from random import random
from arcade import Sprite
from pymunk import Body, Circle, ShapeFilter
from dracarys.constants import SPRITE_LIST_DYNAMIC, CAT_ANIMAL, CAT_DRAGON_FLY, CAT_DRAGON_WALK, CAT_WALL, CAT_ROCK


class Key:
    def __init__(self, game):
        self.game = game

        # Setup PyMunk body and shape
        self.body = Body()
        self.body.position = (
            # TODO: Don't put one on top of rock/tower
            random() * self.game.params.world.width,
            random() * self.game.params.world.height
        )
        self.body.angle = random() * 360
        # TODO: Update this to a box.
        self.shape = Circle(self.body, radius=16)
        self.shape.mass = 0.05
        self.shape.friction = 0.1
        self.shape.filter = ShapeFilter(
            categories=CAT_ANIMAL,
            mask=CAT_ROCK | CAT_WALL | CAT_DRAGON_WALK | CAT_DRAGON_FLY
        )
        self.game.world.space.add(self.body, self.shape)

        # Sprite
        self.sprite = Sprite(
            ':resources:images/items/keyYellow.png',
            scale=32 / 128,
            angle=self.body.angle,
            center_x=self.body.position.x,
            center_y=self.body.position.y,
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.sprite)

    def draw(self):
        """Used to draw self onto arcade scene."""
        self.sprite.position = self.body.position
        self.sprite.radians = self.body.angle
