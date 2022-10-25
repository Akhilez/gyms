from __future__ import annotations
import math
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
        self.window = arcade.Window(
            self.game.params.world.width,
            self.game.params.world.height,
            visible=False
        )

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Player")

        # Set up the Camera
        self.camera = arcade.Camera(self.params.width, self.params.height)

    def step(self):
        pass

    def render_for(self, character: Character) -> np.array:
        # Clean up after rendering? https://api.arcade.academy/en/latest/api/texture.html#arcade.cleanup_texture_cache
        # Garbage collection? https://api.arcade.academy/en/latest/api/open_gl.html#arcade.ArcadeContext.gc_mode

        self.window.clear()

        self.draw_world()

        # Draw all objects
        self.draw_objects()

        cx, cy = character.body.position

        # Position the camera
        # self._center_camera_to_player(cx, cy)

        # Draw our Scene
        self.scene.draw()

        # Activate our Camera
        self.camera.use()

        return self.get_screenshot(
            cx,
            cy,
            character.body.angle
        )

    def draw_world(self):
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

    def draw_objects(self):
        self.game.objects_manager.characters[0].draw()

    def get_screenshot(self, x, y, angle):
        diag = self.params.width
        # diag = self.params.width  # + self.params.height  # heuristic
        # x = x - diag // 2
        # y = y - diag // 2
        image = arcade.get_image(x, y, diag, diag)

        # image = image.rotate(math.radians(angle))

        image = np.asarray(image)  # shape (h, w, 4) (RGBA)
        image = image[:, :, :3]  # shape (h, w, 3)  Got rid of alpha channel
        return image

    def _center_camera_to_player(self, x, y):
        self.camera.move_to((
            x - (self.camera.viewport_width / 2),
            y - (self.camera.viewport_height / 2),
        ))
