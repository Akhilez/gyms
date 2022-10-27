from __future__ import annotations
from random import random
from dracarys.objects.animal import Animal
from typing import TYPE_CHECKING, List
from dracarys.objects.arrow import Arrow
from dracarys.objects.crossbow import CrossBow
from dracarys.objects.dragon import Dragon
from dracarys.objects.key import Key

if TYPE_CHECKING:
    from dracarys.game import Game


class ObjectsManager:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.objects_manager
        self.unlocked_gate = False

        self.animals = [Animal(self.game) for _ in range(self.params.n_animals)]
        for animal in self.animals:
            animal.health = random()

        self.crossbows = [CrossBow(self.game, t.center_of_gravity) for t in self.game.world.towers]
        self.arrows: List[Arrow] = []
        self.keys = []
        self.dragons = [Dragon(self.game)]

    def objects(self):
        return *self.dragons, *self.animals, *self.crossbows, *self.arrows, *self.keys

    def step(self):
        for character in self.objects():
            character.step()

        # Clean up any dead characters
        self.animals = self._clean_up_dead(self.animals)
        self.arrows = self._clean_up_dead(self.arrows)

        # Spawn any new characters
        if len(self.animals) < self.params.n_animals:
            self.animals.extend(self.generate_animals(self.params.n_animals - len(self.animals)))

        # If all dragons die, then game ends.
        if len([d for d in self.dragons if d.health > 0]) == 0:
            self.game.episode_manager.ended = True

    def generate_animals(self, n_animals) -> List[Animal]:
        return [Animal(self.game) for _ in range(n_animals)]

    def on_crossbow_destroyed(self):
        """Check if all crossbows are broken, then acquire key"""
        if True: #all([c.burnt >= 1 for c in self.crossbows]):
            self.keys.append(Key(self.game))
            print("key is spawned")

    def _clean_up_dead(self, characters):
        dead = [a for a in characters if a.health <= 0]
        [self.game.world.space.remove(a.shape) for a in dead]
        [a.sprite.kill() for a in dead]
        return [a for a in characters if a.health > 0]
