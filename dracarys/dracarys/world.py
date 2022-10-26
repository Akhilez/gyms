from __future__ import annotations
from typing import TYPE_CHECKING
import arcade
import numpy as np
import pymunk
from pymunk import Space
from dracarys.constants import CAT_WALL
if TYPE_CHECKING:
    from dracarys.game import Game


class World:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.world

        self.space = Space()
        self.space.damping = self.params.damping

        self.boundaries = self._create_boundaries()

    def step(self):
        self.space.step(dt=1.0 / self.game.params.ui.fps)

    def _create_boundaries(self):
        w, h = self.params.width, self.params.height
        boundaries = [
            pymunk.Segment(self.space.static_body, (0, 0), (0, h), 1),
            pymunk.Segment(self.space.static_body, (0, h), (w, h), 1),
            pymunk.Segment(self.space.static_body, (w, h), (w, 0), 1),
            pymunk.Segment(self.space.static_body, (0, 0), (w, 0), 1),
        ]
        for s in boundaries:
            s.elasticity = .9
            s.friction = 0.0
            s.filter = pymunk.ShapeFilter(categories=CAT_WALL)
        self.space.add(*boundaries)

        # Generate Sprites
        side = 128
        sprite = ":resources:images/tiles/dirtCenter.png"
        for layer in range(0, side * 5, side):
            for x in range(-side * 5, self.params.width + (5*side), side):
                # Create bottom wall
                wall = arcade.Sprite(
                    sprite, 1,
                    center_x=x,
                    center_y=-side // 2 - layer,
                    angle=0,
                )
                self.game.ui_manager.scene.add_sprite("Walls", wall)

                # Create top wall
                wall = arcade.Sprite(
                    sprite, 1,
                    center_x=x,
                    center_y=self.params.height + side // 2 + layer,
                    angle=0,
                )
                self.game.ui_manager.scene.add_sprite("Walls", wall)

            for x in range(-side * 5, self.params.height + (5*side), side):
                # Create left wall
                wall = arcade.Sprite(
                    sprite, 1,
                    center_x=-side//2 - layer,
                    center_y=x,
                    angle=0,
                )
                self.game.ui_manager.scene.add_sprite("Walls", wall)

                # Create right wall
                wall = arcade.Sprite(
                    sprite, 1,
                    center_x=self.params.width + side // 2 + layer,
                    center_y=x,
                    angle=0,
                )
                self.game.ui_manager.scene.add_sprite("Walls", wall)
        
        return boundaries


def generate_perlin_noise_2d(shape, res):
    old_shape = list(shape)
    new_shape = []
    for i in range(len(shape)):
        new_shape.append(((shape[i] // res[i]) + 1) * res[i])
    shape = new_shape
    def f(t):
        return 6 * t**5 - 15 * t**4 + 10 * t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0 : res[0] : delta[0], 0 : res[1] : delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
    n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
    noise = np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)

    return noise[:old_shape[0], :old_shape[1]]
