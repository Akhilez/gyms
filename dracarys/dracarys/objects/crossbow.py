import math
from random import random
from arcade import Sprite, load_texture
from dracarys.constants import SPRITE_LIST_DYNAMIC
from dracarys.objects.arrow import Arrow
from dracarys.objects.character import Character
from dracarys.objects.health_bar import HealthBar
from dracarys.utils import get_distance, get_angle

CROSSBOW_SPRITE = 'objects/images/Crossbow.png'
BROKEN_CROSSBOW_SPRITE = 'objects/images/Broken-Crossbow.png'


class CrossBow(Character):
    def __init__(self, game, center):
        super(CrossBow, self).__init__(game)
        self.p = game.params.objects_manager.crossbow
        self.center = center
        self._reloading = 0

        self.angle = random() * math.pi
        self.burnt = 0
        self._broken = False

        # Sprite
        self.sprite = Sprite(
            CROSSBOW_SPRITE,
            scale=self.p.size / 150,
            angle=math.degrees(self.angle),
            center_x=center[0],
            center_y=center[1],
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.sprite)

        # Health bar
        self.health_bar = HealthBar(
            self,
            (self.center[0], self.center[1] + 20),
            width=self.p.size,
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.health_bar.background_box)
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.health_bar.full_box)

    def draw(self):
        if not self._broken:
            self.sprite.radians = self.angle

        if self.burnt >= 1 and not self._broken:
            self._broken = True
            self.sprite.texture = load_texture(file_name=BROKEN_CROSSBOW_SPRITE)

        self.health_bar.position = (self.center[0], self.center[1] + 20)
        self.health_bar.fullness = 1 - min(1, self.burnt)

    def step(self):
        if self._broken:
            return
        self._reloading += 1

        min_distance = 999999
        min_dragon = None
        for dragon in self.game.objects_manager.dragons:
            distance = get_distance(dragon.body.position, self.center)
            if distance < self.p.observable_distance and distance < min_distance:
                min_distance = distance
                min_dragon = dragon

        if min_dragon is not None:
            self.aim(min_dragon)
            if self._reloading > self.p.min_reload_time:
                if random() < self.p.shoot_probability:
                    self.shoot()

    def aim(self, dragon):
        self.angle = get_angle((self.center[0] + 10, self.center[1]), self.center, dragon.shape.bb.center())

    def shoot(self):
        self.game.objects_manager.arrows.append(Arrow(self.game, self.center, self.angle - math.pi / 2))
        self._reloading = 0

    def burn(self):
        self.burnt += self.p.burn_amount
        if not self._broken and self.burnt >= 1:
            # Check if all crossbows are broken, then acquire key
            self.game.objects_manager.on_crossbow_destroyed()
