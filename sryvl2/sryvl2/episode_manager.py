from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sryvl2.game import Game


class EpisodeManager:
    def __init__(self, game: 'Game'):
        self.game = game
        self.params = game.params.episode

        self.timestep = 0
        self.frame = 0
        self.ended = False

    def step(self):
        self.frame += 1
        if self.is_new_timestep():
            self.timestep += 1
            if self.timestep >= self.params.total_episodes:
                self.ended = True

    def is_new_timestep(self):
        return self.frame % self.params.frames_per_timestep == 0
