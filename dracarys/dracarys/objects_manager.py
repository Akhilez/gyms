from __future__ import annotations
from random import random
from dracarys.objects.animal import Animal
from typing import TYPE_CHECKING, List
# from dracarys.objects.crossbow import CrossBow
from dracarys.objects.dragon import Dragon
if TYPE_CHECKING:
    from dracarys.game import Game


class ObjectsManager:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.objects_manager

        self.animals = self.generate_animals(self.params.n_animals)
        for animal in self.animals:
            animal.health = random()

        # self.crossbow = self._generate_characters_crossbow()
        self.dragons = [Dragon(self.game)]

    def step(self):
        for character in (*self.dragons, *self.animals):
            character.step()

        # Clean up any dead characters
        dead_animals = [a for a in self.animals if a.health <= 0]
        [self.game.world.space.remove(a.shape) for a in dead_animals]
        [a.sprite.kill() for a in dead_animals]
        self.animals = [a for a in self.animals if a.health > 0]

        # Spawn any new characters
        if len(self.animals) < self.params.n_animals:
            self.animals.extend(self.generate_animals(self.params.n_animals - len(self.animals)))

    def generate_animals(self, n_animals) -> List[Animal]:
        return [Animal(self.game) for _ in range(n_animals)]
