from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
if TYPE_CHECKING:
    from sryvl2.game import Game
from sryvl2.rules import ACTION_SPACE


class Character:
    def __init__(self, game: Game):
        self.game = game
        self.action_mask = [None, [1, 1]]
        self.has_lost: bool = False

    def policy(self, **_kwargs):
        # TODO: Sample only legal actions
        return ACTION_SPACE.sample()

    def render(self) -> np.array:
        return self.game.ui_manager.render_for(self)
