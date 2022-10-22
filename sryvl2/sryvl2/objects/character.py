from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sryvl2.game import Game
from sryvl2.rules import action_space


class Character:
    def __init__(self, game: Game):
        self.game = game
        self.action_mask = [None, [1, 1]]
        self.has_lost = False

    def policy(self, **_kwargs):
        # TODO: Sample only legal actions
        return action_space.sample()

    def render(self):
        return self.game.ui_manager.render_for(self)
