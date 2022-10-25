import math

import arcade
import pymunk

H = 500
W = 500

FORCE = 500.0
ROTATION_SPEED = 0.005  # radians


class MyWindow(arcade.Window):
    def __init__(self):
        super(MyWindow, self).__init__()
        arcade.set_background_color(arcade.color.AMAZON)
        self.space = pymunk.Space()
        self.space.damping = 0.9

        # Create boundary
        static = [
            pymunk.Segment(self.space.static_body, (50, 50), (50, 450), 5),
            pymunk.Segment(self.space.static_body, (50, 450), (450, 450), 5),
            pymunk.Segment(self.space.static_body, (450, 450), (450, 50), 5),
            pymunk.Segment(self.space.static_body, (50, 50), (450, 50), 5),
        ]
        for s in static:
            s.elasticity = .9
            s.friction = 0.1
        self.space.add(*static)
        self.boundaries = static

        # Create player
        self.player = pymunk.Circle(pymunk.Body(), radius=20)
        self.player.mass = 1
        self.player.body.position = (100, 100)
        self.player.friction = 0.1
        self.space.add(self.player.body, self.player)
        print('moment: ', self.player.body.moment)

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Player")

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/space_shooter/playerShip3_orange.png"
        self.player_sprite = arcade.Sprite(
            image_source,
            scale=40 / 128,
            angle=self.player.body.angle,
            center_x=self.player.body.position.x,
            center_y=self.player.body.position.y,
        )
        self.scene.add_sprite("Player", self.player_sprite)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

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
            # self.player.body.angle += ROTATION_SPEED
            force = (-FORCE, 0)
            self.player.body.apply_force_at_local_point(
                force=force, point=(0, 0)
            )
        elif self.right_pressed and not self.left_pressed:
            # self.player.body.angle -= ROTATION_SPEED
            force = (FORCE, 0)
            self.player.body.apply_force_at_local_point(
                force=force, point=(0, 0)
            )

        velocity = self.player.body.velocity_at_local_point((0, 0))
        velocity_angle = self.get_angle((0, 1), (0, 0), velocity)
        rotation = min(velocity_angle, ROTATION_SPEED)
        if velocity.x < 0:
            self.player.body.angle += rotation
        elif velocity.x > 0:
            self.player.body.angle -= rotation
        self.space.step(dt)

        # Position the camera
        self.center_camera_to_player()

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

        self.player_sprite.position = self.player.body.position
        self.player_sprite.radians = self.player.body.angle

        # Draw our Scene
        self.scene.draw()

        # Activate our Camera
        self.camera.use()

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

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # # Don't let camera travel past 0
        # if screen_center_x < 0:
        #     screen_center_x = 0
        # if screen_center_y < 0:
        #     screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    @staticmethod
    def get_angle(a, b, c):
        ang = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
        return abs(ang)


if __name__ == '__main__':
    # TODO: Factoring rotation and force = have controls to rotate and move.
    window = MyWindow()
    arcade.run()
    # print(MyWindow.get_angle((0, 1), (0, 0), (1, 0)))
