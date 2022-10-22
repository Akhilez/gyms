from sryvl2.game import Game


class UIManager:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.ui

    def step(self):
        pass
