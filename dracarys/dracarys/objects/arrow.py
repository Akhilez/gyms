from __future__ import annotations
import math
from typing import TYPE_CHECKING
from arcade import Sprite
from pymunk import Body, Circle, ShapeFilter, Shape
from dracarys.constants import (
    SPRITE_LIST_DYNAMIC, CAT_ARROW, CAT_TOWER, CAT_WALL,
    CAT_DRAGON_WALK, CAT_DRAGON_FLY, CAT_ROCK
)
if TYPE_CHECKING:
    from dracarys.game import Game
from dracarys.objects.character import Character


class Arrow(Character):
    def __init__(self, game: Game, center, angle):
        super(Arrow, self).__init__(game)
        self.p = game.params.objects_manager.arrow
        self.radians = angle

        # Setup PyMunk body and shape
        self.body = Body()
        self.body.position = center
        self.shape = Circle(self.body, radius=self.p.size)
        self.shape.mass = self.p.initial_mass
        self.shape.friction = 0.0
        self.shape.filter = ShapeFilter(
            # group=CAT_TOWER,
            categories=CAT_ARROW,
            # Collide with all except animal and tower
            mask=CAT_WALL | CAT_DRAGON_WALK | CAT_DRAGON_FLY | CAT_ROCK
        )
        self.body.angle = angle
        self.shape.parent = self
        self.game.world.space.add(self.body, self.shape)

        # Sprite
        self.sprite = Sprite(
            ':resources:images/space_shooter/laserBlue01.png',
            scale=self.p.size / 64,
            angle=math.degrees(angle + math.pi / 2),
            center_x=self.body.position.x,
            center_y=self.body.position.y,
        )
        self.game.ui_manager.scene.add_sprite(SPRITE_LIST_DYNAMIC, self.sprite)

        self.body.apply_impulse_at_local_point((0, self.p.impulse), point=(0, 0))

    def draw(self):
        self.sprite.position = self.body.position

    def step(self):
        vx, vy = self.body.velocity
        if abs(vx) + abs(vy) < 50:
            self.health = 0

    def on_collision(self, _):
        self.health = 0
