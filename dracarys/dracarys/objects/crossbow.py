from random import random
from arcade import Sprite, load_texture
from pymunk import Body, Circle, ShapeFilter
from pymunk._chipmunk.lib import CP_BODY_TYPE_STATIC
from dracarys.constants import SPRITE_LIST_DYNAMIC
from dracarys.objects.character import Character
from dracarys.utils import get_distance

CROSSBOW_SPRITE = 'objects/images/Crossbow.png'
BROKEN_CROSSBOW_SPRITE = 'objects/images/Broken-Crossbow.png'


class CrossBow(Character):
    def __init__(self, game, center):
        super(CrossBow, self).__init__(game)
        self.p = game.params.objects_manager.crossbow
        self.center = center

        self.angle = random() * 360
        self.burnt = 0
        self._broken = False

        # Setup PyMunk body and shape
        # self.body = Body(body_type=CP_BODY_TYPE_STATIC)
        # self.body.position = position
        # self.body.angle = random() * 360
        # self.shape = Circle(self.body, radius=self.p.size)
        # self.shape.mass = self.p.initial_mass
        # self.shape.friction = 0.0
        # self.shape.filter = ShapeFilter(mask=0)
        # self.game.world.space.add(self.body, self.shape)

        # Sprite
        self.sprite = Sprite(
            CROSSBOW_SPRITE,
            scale=self.p.size / 150,
            angle=self.angle,
            center_x=center[0],
            center_y=center[1],
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.sprite)

    def draw(self):
        if not self._broken:
            self.sprite.radians = self.angle

        if self.burnt >= 1 and not self._broken:
            self._broken = True
            self.sprite.texture = load_texture(file_name=BROKEN_CROSSBOW_SPRITE)

    def step(self):
        min_distance = 999999
        min_dragon = None
        for dragon in self.game.objects_manager.dragons:
            distance = get_distance(dragon.body.position, self.center)
            if distance < self.p.observable_distance and distance < min_distance:
                min_distance = distance
                min_dragon = dragon

        if min_dragon is not None:
            self.aim(min_dragon)
            if random() < self.p.shoot_probability():
                self.shoot(min_dragon)

    def aim(self, dragon):
        # TODO: Aim
        pass

    def shoot(self, dragon):
        # TODO: Shoot
        pass
