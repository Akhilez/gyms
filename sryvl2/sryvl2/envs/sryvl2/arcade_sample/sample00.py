"""
Platformer Game
"""
from random import random

import arcade

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Platformer"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, visible=True)

        self.wall_list = None
        self.player_list = None

        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/space_shooter/playerShip3_orange.png"
        self.player_sprite = arcade.Sprite(
            image_source,
            CHARACTER_SCALING,
            angle=random() * 360,
            center_x=random() * SCREEN_WIDTH,
            center_y=random() * SCREEN_HEIGHT,
        )
        self.player_list.append(self.player_sprite)

        # Create bottom wall
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, SCREEN_WIDTH + 64, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Create left wall
        for x in range(0, SCREEN_HEIGHT + 64, 64):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                TILE_SCALING,
                center_x=32,
                center_y=x,
                angle=270,
            )
            self.wall_list.append(wall)

        # Create right wall
        for x in range(0, SCREEN_HEIGHT + 64, 64):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                TILE_SCALING,
                center_x=SCREEN_WIDTH - 32,
                center_y=x,
                angle=90,
            )
            self.wall_list.append(wall)

        # Create top wall
        for x in range(0, SCREEN_HEIGHT + 64, 64):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                TILE_SCALING,
                center_x=x,
                center_y=SCREEN_WIDTH - 32,
                angle=180,
            )
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[250, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.wall_list.append(wall)


    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here

        # Draw our sprites
        self.wall_list.draw()
        self.player_list.draw()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
