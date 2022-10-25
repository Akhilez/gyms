from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dracarys.game import Game
import numpy as np
from dracarys.objects.character import Character
import arcade


class UIManager:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.ui
        self.window = arcade.Window(self.params.width, self.params.height, visible=False)

    def step(self):
        pass

    def render_for(self, character: Character) -> np.array:
        # Clean up after rendering? https://api.arcade.academy/en/latest/api/texture.html#arcade.cleanup_texture_cache
        # Garbage collection? https://api.arcade.academy/en/latest/api/open_gl.html#arcade.ArcadeContext.gc_mode

        self.window.clear()
        arcade.draw_rectangle_filled(50, 50, 50, 50, color=arcade.color.AMAZON)
        image = arcade.get_image(0, 0, *self.window.get_size())
        image = np.asarray(image)  # shape (h, w, 4) (RGBA)
        image = image[:, :, :3]  # shape (h, w, 3)  Got rid of alpha channel
        return image
