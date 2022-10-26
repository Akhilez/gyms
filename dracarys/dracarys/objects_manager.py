from __future__ import annotations

from dracarys.objects.animals.animal import Animal
from typing import TYPE_CHECKING

# from dracarys.objects.crossbow import CrossBow
# from dracarys.objects.dragon import Dragon

from dracarys.objects.dragon import Dragon
if TYPE_CHECKING:
    from dracarys.game import Game


class ObjectsManager:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.objects_manager


        # self.dragons = self._generate_characters_dragon()
        self.animals = [self.generate_characters_animal()]
        # self.crossbow = self._generate_characters_crossbow()

        self.dragons = [Dragon(self.game)]

    def step(self):
        for character in self.dragons:
            character.step()
        # Clean up any dead dragons
        # Spawn any new dragons

    # def _generate_characters_dragon(self) -> List[Dragon]:
    #     return [Dragon(self.game)]
    #
    def generate_characters_animal(self) -> Animal:
        return Animal(self.game)
    #
    # def _generate_characters_crossbow(self) -> List[CrossBow]:
    #     return [CrossBow(self.game)]
