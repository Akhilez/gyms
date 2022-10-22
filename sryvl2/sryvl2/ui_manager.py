from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sryvl2.game import Game
import numpy as np
from sryvl2.objects.character import Character


class UIManager:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.ui

    def step(self):
        pass

    def render_for(self, character: Character) -> np.array:
        return np.random.random((self.params.height, self.params.width, 3)) * 55 + 200
