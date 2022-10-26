from __future__ import annotations
from typing import List
from dracarys.objects.character import Character
from typing import TYPE_CHECKING
from dracarys.objects.dragon import Dragon
if TYPE_CHECKING:
    from dracarys.game import Game


class ObjectsManager:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.objects_manager
        self.dragons = [Dragon(self.game)]

    def step(self):
        for character in self.dragons:
            character.step()
        # Clean up any dead dragons
        # Spawn any new dragons
