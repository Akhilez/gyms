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
        self.camera = arcade.Camera(self.game.params.world.width, self.game.params.world.width)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

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
        self._center_camera_to_player(cx, cy)

        # Draw our Scene
        self.scene.draw()

        # Activate our Camera
        self.camera.use()

        return self.get_screenshot(character.body.angle)

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

    def get_screenshot(self, angle):
        w = self.params.width * 2
        h = self.params.height * 2
        image = arcade.get_image(0, 0, w, h)

        image = image.rotate(-math.degrees(angle))
        # image = image.resize((self.params.width, self.params.height))

        image = np.asarray(image)  # shape (h, w, 4) (RGBA)
        image = image[:, :, :3]  # shape (h, w, 3)  Got rid of alpha channel
        image = image[w // 4: w // 4 * 3, h // 4: h // 4 * 3, :]
        return image

    def _center_camera_to_player(self, x, y):
        screen_center_x = x - (self.camera.viewport_width / 2)
        screen_center_y = y - (self.camera.viewport_height / 2)

        # # Don't let camera travel past 0
        # if screen_center_x < 0:
        #     screen_center_x = 0
        # if screen_center_y < 0:
        #     screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)
