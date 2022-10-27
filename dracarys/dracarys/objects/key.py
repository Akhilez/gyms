from random import random
from arcade import Sprite
from pymunk import Body, Circle, ShapeFilter
from dracarys.constants import SPRITE_LIST_DYNAMIC, CAT_ANIMAL, CAT_DRAGON_FLY, CAT_DRAGON_WALK, CAT_WALL, CAT_ROCK
from dracarys.objects.character import Character


class Key(Character):
    def __init__(self, game):
        super(Key, self).__init__(game)
        self.acquired_by = None

        # Setup PyMunk body and shape
        self.body = Body()
        self.body.position = self._get_random_ground_position()
        self.body.angle = random() * 360
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

    def step(self):
        if self.game.objects_manager.unlocked_gate:
            self.body.position = self.game.world.gate.body.position
        elif self.acquired_by is not None:
            self.body.position = self.acquired_by.body.position
