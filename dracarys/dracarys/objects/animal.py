from __future__ import annotations
from enum import Enum
from random import random
from typing import TYPE_CHECKING
import arcade
from arcade import Sprite
from pymunk import Body, Circle, ShapeFilter
from dracarys.constants import CAT_ANIMAL, SPRITE_LIST_DYNAMIC, DRAGON_ACTION_SPACE
from dracarys.objects.health_bar import HealthBar
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
        self.body.position = self._get_random_ground_position()
        self.body.angle = random() * 360
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

        self.health_bar: HealthBar = HealthBar(
            self,
            self.shape.bb.center(),
            width=self.p.size,
            height=self.p.size//6
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.health_bar.background_box)
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.health_bar.full_box)

    def draw(self):
        """Used to draw self onto arcade scene."""
        self.sprite.position = self.body.position
        self.sprite.radians = self.body.angle

        self.health_bar.position = self.shape.bb.center()
        self.health_bar.background_box.radians = self.body.angle
        self.health_bar.full_box.radians = self.body.angle
        self.health_bar.background_box.radians = self.body.angle
        self.health_bar.fullness = 1 - min(1, self.burnt)

        if self.burnt >= 1 and not self._flipped:
            self._flipped = True
            self.sprite.texture = arcade.load_texture(file_name=ANIMAL_DOWN_SPRITES[self.type])

        if self._is_in_water():
            self.health = 0

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

    def _is_in_water(self):
        x = self.body.position[0] // self.game.params.world.cell_size
        y = self.body.position[1] // self.game.params.world.cell_size

        return (x, y) in zip(*self.game.world.water)
