from sryvl2.game import Game


class Stats:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.stats

    def step(self):
        pass
