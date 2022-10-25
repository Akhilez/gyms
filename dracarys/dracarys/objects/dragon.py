import arcade
import character


class Dragon(character):
    def __init__(self):
        self.power = 5
        self.drag_level = 0


    def draw(self):
        """Used to draw self onto arcade scene."""
        arcade.draw_circle_filled(
            center_x=self.body.position.x,
            center_y=self.body.position.y,
            radius=self.shape.radius,
            color=arcade.color.RED,
        )
        self.player_sprite.position = self.body.position
        self.player_sprite.radians = self.body.angle