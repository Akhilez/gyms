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

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Player")

    def step(self):
        pass

    def render_for(self, character: Character) -> np.array:
        # Clean up after rendering? https://api.arcade.academy/en/latest/api/texture.html#arcade.cleanup_texture_cache
        # Garbage collection? https://api.arcade.academy/en/latest/api/open_gl.html#arcade.ArcadeContext.gc_mode

        self.window.clear()

        # Create boundaries
        # This shows using a loop to place multiple sprites horizontally
        for s in self.game.world.boundaries:
            arcade.draw_line(
                start_x=s.a.x,
                start_y=s.a.y,
                end_x=s.b.x,
                end_y=s.b.y,
                color=arcade.color.TAN,
                line_width=s.radius,
            )

        self.game.objects_manager.characters[0].draw()

        # Draw our Scene
        self.scene.draw()

        image = arcade.get_image(0, 0, *self.window.get_size())
        image = np.asarray(image)  # shape (h, w, 4) (RGBA)
        image = image[:, :, :3]  # shape (h, w, 3)  Got rid of alpha channel
        return image
