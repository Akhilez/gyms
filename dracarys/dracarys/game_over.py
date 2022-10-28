import arcade

from dracarys.game import Game


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, game: Game):
        """ This is run once when we switch to this view """
        super().__init__()
        self.game = game
        self.texture = arcade.load_texture("objects/images/dragon-1-sitting.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.game.params.world.width - 1, 0, self.game.params.world.height - 1)

    def on_draw(self):
        """ Draw this view """
        self.game.ui_manager.window.clear()
        self.clear()
        self.texture.draw_sized(self.game.params.world.width / 2, self.game.params.world.height / 2,
                                self.game.params.world.width, self.game.params.world.height)

    # def on_mouse_press(self, _x, _y, _button, _modifiers):
    #     """ If the user presses the mouse button, re-start the game. """
    #     game_view = GameView()
    #     game_view.setup()
    #     self.window.show_view(game_view)