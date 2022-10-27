from __future__ import annotations
from enum import Enum
from random import random
from typing import TYPE_CHECKING
import arcade
from arcade import Sprite
from pymunk import Body, Circle, ShapeFilter
from dracarys.constants import CAT_ANIMAL, SPRITE_LIST_DYNAMIC, DRAGON_ACTION_SPACE
if TYPE_CHECKING:
    from dracarys.game import Game
from dracarys.objects.character import Character


class AnimalTypes(Enum):
    COW1 = 'cow1'
    COW2 = 'cow2'
    COW3 = 'cow3'
    DEER = 'deer'
    GOAT = 'goat'

    @staticmethod
    def sample():
        all_types = list(AnimalTypes)
        return all_types[int(random() * len(all_types))]


ANIMAL_SPRITES = {
    AnimalTypes.COW1: 'objects/images/cow-1.png',
    AnimalTypes.COW2: 'objects/images/cow-2.png',
    AnimalTypes.COW3: 'objects/images/cow-3.png',
    AnimalTypes.DEER: 'objects/images/deer.png',
    AnimalTypes.GOAT: 'objects/images/goat.png',
}

ANIMAL_DOWN_SPRITES = {
    AnimalTypes.COW1: 'objects/images/cow-1-horizontal.png',
    AnimalTypes.COW2: 'objects/images/cow-2-horizontal.png',
    AnimalTypes.COW3: 'objects/images/cow-3-horizontal.png',
    AnimalTypes.DEER: 'objects/images/deer-horizontal.png',
    AnimalTypes.GOAT: 'objects/images/goat-horizontal.png',
}


class Animal(Character):
    def __init__(self, game: Game):
        super(Animal, self).__init__(game)
        self.type = AnimalTypes.sample()
        self.p = game.params.objects_manager.animal

        self.action_space = DRAGON_ACTION_SPACE
        self.burnt = 0
        self._flipped = False

        # Setup PyMunk body and shape
        self.body = Body()
        self.body.position = (
            # TODO: Don't put one on top of rock/tower
            random() * self.game.params.world.width,
            random() * self.game.params.world.height
        )
        self.body.angle = random() * 360
        # TODO: Update this to a box.
        self.shape = Circle(self.body, radius=self.p.size)
        self.shape.mass = self.p.initial_mass
        self.shape.friction = 0.0
        self.shape.filter = ShapeFilter(categories=CAT_ANIMAL)
        self.game.world.space.add(self.body, self.shape)

        # Sprite
        self.sprite = Sprite(
            ANIMAL_SPRITES[self.type],
            scale=self.p.size / 128,
            angle=self.body.angle,
            center_x=self.body.position.x,
            center_y=self.body.position.y,
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.sprite)

    def draw(self):
        """Used to draw self onto arcade scene."""
        self.sprite.position = self.body.position
        self.sprite.radians = self.body.angle

        if self.burnt >= 1 and not self._flipped:
            self._flipped = True
            self.sprite.texture = arcade.load_texture(file_name=ANIMAL_DOWN_SPRITES[self.type])

    def step(self):
        actions = self.policy(game=self.game)
        (x, y, r), a = actions

        # Force
        force = (x * self.p.force_max, abs(y) * self.p.force_max)
        self.body.apply_force_at_local_point(force=force, point=(0, 0))

        # Rotation
        rotation = self.p.rotation_max_speed * r
        self.body.angle -= rotation

        self.health -= self.p.health_decay_rate

    def burn(self):
        self.burnt += self.p.burn_amount
