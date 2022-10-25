from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dracarys.game import Game
from gym.spaces import Tuple, Discrete, Box


ACTION_SPACE = Tuple(
    (
        Box(-1, 1, shape=(3,)),  # Force direction x, y and rotation direction r
        Discrete(3),  # Action index (like fire, eat)
    ),
)


class Rules:
    def __init__(self, game: Game):
        self.game = game

    def step(self):
        pass

    def game_period(self):
        return 600  # 10 minutes
        pass

    def health_degen(self, dragon):
        # based of health of the character
        # assume health is 500 - decrement occurs every unit time
        # if flying - decrement 4 times normal
        # walking - decrement 2 times normal
        # stationary - decrement single unit
        decrement_const = 1
        if dragon.drag_level == 2:
            # flying without eating will kill you in 25 seconds
            dragon.health -= decrement_const * 4

        if dragon.drag_level == 1:
            # walking will kill you in 50 seconds without eating
            dragon.health -= decrement_const * 2

        if dragon.drag_level == 0:
            # doing nothing will kill you in 1 minute 40 seconds without eating
            dragon.health -= decrement_const

    def cook_time(self, dragon, animal):
        # assume power will be like 5 and animal health will be like 15 max. Should take max 3 seconds
        return animal.health/dragon.power

    def eat(self, dragon, animal):
        if dragon.health > 90:
            # almost full so we can start to store
            self.food_storage(dragon, animal.health)
        else:
            dragon.health += animal.health

    # attack and defense can be the same, maybe. Just swap between drag and opponent
    def attack_mode(self, dragon, opponent):
        # a player can only attack for 3 seconds at a time
        opponent.health = opponent.health - (dragon.power * 3)
        if dragon.health < 0:
                # dead - execute some sort of dead rule/ event

    def food_storage(self, dragon, storage):
        dragon.storage += storage
