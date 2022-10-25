import pygame
from sryvl2.game import Game


class App:
    def __init__(self):
        pygame.init()
        self._game = Game(params='human_single_player')
        self.p = self._game.params
        self.player = self._game.objects_manager.characters[0]
        self._display = pygame.display.set_mode(
            (self.p.ui.width, self.p.ui.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._clock = pygame.time.Clock()
        self._running = True

        self.actions = [0.0, 0.0, 0]

        self.player.policy = lambda **_: self.actions

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        # TODO: Read keyboard events or something and set actions.
        #       Also reset when keys are released.
        self.actions = [0.0, 0.1, 0]

    def on_loop(self):
        if self.player.has_lost:
            self._running = False

    def on_render(self):
        image = self.player.render()
        # print(image.shape)
        self._display.blit(pygame.surfarray.make_surface(image), (0, 0))
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while self._running:
            self._clock.tick(self.p.ui.fps)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
