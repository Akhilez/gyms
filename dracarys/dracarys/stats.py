from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sryvl2.game import Game


class Stats:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.stats

    def step(self):
        pass
