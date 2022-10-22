from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sryvl2.game import Game
from gym.spaces import Tuple, Discrete, Box


action_space = Tuple((Box(-1, 1, shape=(2,)), Discrete(2)))


class Rules:
    def __init__(self, game: Game):
        self.game = game

    def step(self):
        pass
