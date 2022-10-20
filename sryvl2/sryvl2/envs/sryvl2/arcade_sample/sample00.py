"""
Platformer Game
"""
import math
from random import random

import arcade

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Platformer"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

ANGLE_CHANGE = 10

# Speed limit
MAX_SPEED = 300

# How fast we accelerate
ACCELERATION_RATE = 5

# How fast to slow down after we let off the key
FRICTION = 0.2


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, visible=True)

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # Our Scene Object
        self.scene = None

        self.player_sprite = None
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):
        # Initialize Scene
        self.scene = arcade.Scene()

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/space_shooter/playerShip3_orange.png"
        self.player_sprite = arcade.Sprite(
            image_source,
            CHARACTER_SCALING,
            angle=random() * 360,
            center_x=random() * SCREEN_WIDTH,
            center_y=random() * SCREEN_HEIGHT,
        )
        self.scene.add_sprite("Player", self.player_sprite)
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )

        # Create bottom wall
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, SCREEN_WIDTH + 64, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Create left wall
        for x in range(0, SCREEN_HEIGHT + 64, 64):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                TILE_SCALING,
                center_x=32,
                center_y=x,
                angle=270,
            )
            self.scene.add_sprite("Walls", wall)

        # Create right wall
        for x in range(0, SCREEN_HEIGHT + 64, 64):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                TILE_SCALING,
                center_x=SCREEN_WIDTH - 32,
                center_y=x,
                angle=90,
            )
            self.scene.add_sprite("Walls", wall)

        # Create top wall
        for x in range(0, SCREEN_HEIGHT + 64, 64):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                TILE_SCALING,
                center_x=x,
                center_y=SCREEN_WIDTH - 32,
                angle=180,
            )
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[250, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            # self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            angle = self.player_sprite.radians+(math.pi / 2)
            print(self.player_sprite.radians)
            self.player_sprite.change_x = math.cos(angle) * PLAYER_MOVEMENT_SPEED
            self.player_sprite.change_y = math.sin(angle) * PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.angle += ANGLE_CHANGE
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.angle -= ANGLE_CHANGE

        if key == arcade.key.F:
            self.player_sprite.forward(5)

        if key == arcade.key.X:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = 0

        # # Add some friction
        # if self.player_sprite.change_x > FRICTION:
        #     self.player_sprite.change_x -= FRICTION
        # elif self.player_sprite.change_x < -FRICTION:
        #     self.player_sprite.change_x += FRICTION
        # else:
        #     self.player_sprite.change_x = 0
        #
        # if self.player_sprite.change_y > FRICTION:
        #     self.player_sprite.change_y -= FRICTION
        # elif self.player_sprite.change_y < -FRICTION:
        #     self.player_sprite.change_y += FRICTION
        # else:
        #     self.player_sprite.change_y = 0
        #
        # # Apply acceleration based on the keys pressed
        # if key == arcade.key.UP or key == arcade.key.W:
        #     self.player_sprite.change_y += ACCELERATION_RATE
        #     # self.physics_engine.apply_force(self.player_sprite, (0, ACCELERATION_RATE))
        # elif key == arcade.key.DOWN or key == arcade.key.S:
        #     self.player_sprite.change_y += -ACCELERATION_RATE
        # elif key == arcade.key.LEFT or key == arcade.key.A:
        #     self.player_sprite.change_x += -ACCELERATION_RATE
        # elif key == arcade.key.RIGHT or key == arcade.key.D:
        #     self.player_sprite.change_x += ACCELERATION_RATE
        #
        # if self.player_sprite.change_x > MAX_SPEED:
        #     self.player_sprite.change_x = MAX_SPEED
        # elif self.player_sprite.change_x < -MAX_SPEED:
        #     self.player_sprite.change_x = -MAX_SPEED
        # if self.player_sprite.change_y > MAX_SPEED:
        #     self.player_sprite.change_y = MAX_SPEED
        # elif self.player_sprite.change_y < -MAX_SPEED:
        #     self.player_sprite.change_y = -MAX_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        self.player_sprite.change_y = 0
        self.player_sprite.change_x = 0
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here

        # Draw our Scene
        self.scene.draw()

        # Activate our Camera
        self.camera.use()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        # # Don't let camera travel past 0
        # if screen_center_x < 0:
        #     screen_center_x = 0
        # if screen_center_y < 0:
        #     screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
