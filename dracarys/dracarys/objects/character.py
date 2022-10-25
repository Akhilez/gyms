from __future__ import annotations
from random import random
from typing import TYPE_CHECKING
import numpy as np
from pymunk import Body, Circle
if TYPE_CHECKING:
    from dracarys.game import Game
from dracarys.rules import ACTION_SPACE


class Character:
    def __init__(self, game: Game):
        self.game = game
        self.p = game.params.objects_manager.character

        self.action_mask = [None, [1, 1]]
        self.has_lost: bool = False

        self.body = Body()
        self.body.position = (
            random() * self.game.params.world.width,
            random() * self.game.params.world.height
        )
        self.shape = Circle(self.body, radius=self.p.size)
        self.shape.mass = self.p.initial_mass
        self.shape.friction = 1
        self.game.world.space.add(self.body, self.shape)

    def policy(self, **_kwargs):
        # TODO: Sample only legal actions
        return ACTION_SPACE.sample()

    def render(self) -> np.array:
        return self.game.ui_manager.render_for(self)
