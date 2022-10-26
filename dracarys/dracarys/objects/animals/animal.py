from __future__ import annotations

from random import randrange
from typing import TYPE_CHECKING

from dracarys.objects.animals.cows import Cows
from dracarys.objects.animals.deers import Deer
from dracarys.objects.animals.goats import Goats

if TYPE_CHECKING:
    from dracarys.game import Game
from dracarys.objects.character import Character


class Animal(Character):
    def __init__(self, game: Game):
        super(Animal, self).__init__(game)
        self.drawn = False

    def draw(self):
        if not self.drawn:
            animal_types = ["Cow", "Goat", "Deer"]
            index = randrange(3)
            print(index)

            if animal_types[index] == "Cow":
                Cows(self.game).draw()
            if animal_types[index] == "Goat":
                Goats(self.game).draw()
            if animal_types[index] == "Deer":
                Deer(self.game).draw()

            self.drawn = True


