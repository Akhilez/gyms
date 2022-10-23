import arcade
import pymunk

H = 500
W = 500

FORCE = 500.0


class MyWindow(arcade.Window):
    def __init__(self):
        super(MyWindow, self).__init__()
        arcade.set_background_color(arcade.color.AMAZON)
        self.space = pymunk.Space()
        self.space.damping = 0.9
        static = [
            pymunk.Segment(self.space.static_body, (50, 50), (50, 450), 5),
            pymunk.Segment(self.space.static_body, (50, 450), (450, 450), 5),
            pymunk.Segment(self.space.static_body, (450, 450), (450, 50), 5),
            pymunk.Segment(self.space.static_body, (50, 50), (450, 50), 5),
        ]
        for s in static:
            s.elasticity = .9
        self.space.add(*static)
        self.boundaries = static

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Create player
        self.player = pymunk.Circle(pymunk.Body(), radius=20)
        self.player.mass = 1
        self.player.body.position = (100, 100)
        self.player.friction = 0.1
        self.space.add(self.player.body, self.player)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def on_update(self, dt):
        if self.up_pressed and not self.down_pressed:
            force = (0, FORCE)
            self.player.body.apply_force_at_local_point(
                force=force, point=(0, 0)
            )
        elif self.down_pressed and not self.up_pressed:
            force = (0, -FORCE)
            self.player.body.apply_force_at_local_point(
                force=force, point=(0, 0)
            )
        if self.left_pressed and not self.right_pressed:
            force = (-FORCE, 0)
            self.player.body.apply_force_at_local_point(
                force=force, point=(0, 0)
            )
        elif self.right_pressed and not self.left_pressed:
            force = (FORCE, 0)
            self.player.body.apply_force_at_local_point(
                force=force, point=(0, 0)
            )
        self.space.step(dt)

    def on_draw(self):
        self.clear()

        # Create boundaries
        # This shows using a loop to place multiple sprites horizontally
        for s in self.boundaries:
            arcade.draw_line(
                start_x=s.a.x,
                start_y=s.a.y,
                end_x=s.b.x,
                end_y=s.b.y,
                color=arcade.color.TAN,
                line_width=s.radius,
            )

        arcade.draw_circle_filled(
            center_x=self.player.body.position.x,
            center_y=self.player.body.position.y,
            radius=self.player.radius,
            color=arcade.color.RED,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


if __name__ == '__main__':
    window = MyWindow()
    arcade.run()
