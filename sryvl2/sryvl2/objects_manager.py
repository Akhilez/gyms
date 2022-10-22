from typing import List
from sryvl2.objects.character import Character
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sryvl2.game import Game


class ObjectsManager:
    def __init__(self, game: 'Game'):
        self.game = game
        self.params = game.params.objects_manager
        self.characters = self._generate_characters()

    def step(self):
        pass

    def _generate_characters(self) -> List[Character]:
        return [Character(self.game)]
