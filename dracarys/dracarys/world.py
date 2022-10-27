from __future__ import annotations

from os.path import join
from random import random
from typing import TYPE_CHECKING
import arcade
import numpy as np
import pymunk
from pymunk import Space
from dracarys.collisions import collision_post
from dracarys.constants import CAT_WALL, CAT_ROCK, CAT_TOWER, CAT_ARROW, BASE_DIR

if TYPE_CHECKING:
    from dracarys.game import Game
from dracarys.constants import SPRITE_LIST_STATIC


class World:
    def __init__(self, game: Game):
        self.game = game
        self.params = game.params.world

        self.space = Space()
        self.space.damping = self.params.damping

        self.boundaries = self._create_boundaries()
        self.hills = None
        (
            self.hill_indices,
            self.slopes,
            self.ground,
            self.sand,
            self.grass,
            self.water,
        ) = self._create_terrain()

        self.towers = self._create_towers()
        self.gate = self._create_gate()

        self.collision_handler = self.space.add_default_collision_handler()
        self.collision_handler.post_solve = collision_post

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
        sprite = join(BASE_DIR, "objects/images/Stone-1.png")
        for layer in range(0, side * 5, side):
            for x in range(-side * 5, self.params.width + (5 * side), side):
                # Create bottom wall
                wall = arcade.Sprite(
                    sprite, 1,
                    center_x=x,
                    center_y=-side // 2 - layer,
                    angle=0,
                )
                self.game.ui_manager.scene.add_sprite(SPRITE_LIST_STATIC, wall)

                # Create top wall
                wall = arcade.Sprite(
                    sprite, 1,
                    center_x=x,
                    center_y=self.params.height + side // 2 + layer,
                    angle=0,
                )
                self.game.ui_manager.scene.add_sprite(SPRITE_LIST_STATIC, wall)

            for x in range(-side * 5, self.params.height + (5 * side), side):
                # Create left wall
                wall = arcade.Sprite(
                    sprite, 1,
                    center_x=-side // 2 - layer,
                    center_y=x,
                    angle=0,
                )
                self.game.ui_manager.scene.add_sprite(SPRITE_LIST_STATIC, wall)

                # Create right wall
                wall = arcade.Sprite(
                    sprite, 1,
                    center_x=self.params.width + side // 2 + layer,
                    center_y=x,
                    angle=0,
                )
                self.game.ui_manager.scene.add_sprite(SPRITE_LIST_STATIC, wall)

        return boundaries

    def _create_terrain(self):
        # 1. Get perlin noise
        perlin_resolution = 4
        terrain_w = self.params.width // self.params.cell_size
        terrain_h = self.params.height // self.params.cell_size
        terrain = generate_perlin_noise_2d((terrain_w, terrain_h), [perlin_resolution] * 2)

        # 2. Divide it into hill, slope, ground, grass and water
        hills, slopes, ground, sand, grass, water = self._discretize_terrain(terrain)

        # 3. Make static bodies of hills
        self.hills = self._make_hills(hills, ':resources:images/tiles/stoneCenter.png')

        # 4. Make shapes of rest
        self._make_grid(slopes, ':resources:images/tiles/planetCenter.png')
        self._make_grid(ground, ':resources:images/tiles/sandCenter.png')
        self._make_grid(sand, ':resources:images/topdown_tanks/tileSand2.png', sprite_side=64)
        self._make_grid(grass, ':resources:images/topdown_tanks/tileGrass2.png', sprite_side=64)
        self._make_grid(water, ':resources:images/tiles/water.png')
        # self.space.add(*slopes, *ground, *grass, *water)

        return hills, slopes, ground, grass, sand, water

    def _make_grid(self, indices, sprite, sprite_side=128):
        s = self.params.cell_size
        for x, y in zip(*indices):
            x *= s
            y *= s
            cell = arcade.Sprite(
                sprite,
                scale=s / sprite_side,
                center_x=x + s // 2,
                center_y=y + s // 2,
            )
            self.game.ui_manager.scene.add_sprite(SPRITE_LIST_STATIC, cell)

    def _make_hills(self, hill_indices, sprite):
        s = self.params.cell_size
        sprite_side = 128
        hills = []
        for x, y in zip(*hill_indices):
            x *= s
            y *= s
            hill = pymunk.Poly(
                self.space.static_body,
                # [(0, 0), (s, 0), (s, s), (0, s)]
                [(x, y), (x + s, y), (x + s, y + s), (x, y + s)],
            )
            # hill.body.position = (x, y)
            hill.elasticity = 0.9
            hill.friction = 0.0
            hill.filter = pymunk.ShapeFilter(group=CAT_ROCK, categories=CAT_ROCK)
            hills.append(hill)

            cell = arcade.Sprite(
                sprite,
                scale=s / sprite_side,
                center_x=x + s // 2,
                center_y=y + s // 2,
            )
            self.game.ui_manager.scene.add_sprite(SPRITE_LIST_STATIC, cell)
        self.space.add(*hills)
        return hills

    def _create_towers(self):
        s = self.params.tower_size
        towers = []
        terrain_w = self.params.width // self.params.cell_size
        terrain_h = self.params.height // self.params.cell_size
        while len(towers) < self.params.n_towers:
            x = int(random() * terrain_w)
            y = int(random() * terrain_h)
            if (x, y) in zip(*self.hill_indices):
                continue

            x *= self.params.cell_size
            y *= self.params.cell_size
            tower = pymunk.Poly(
                self.space.static_body,
                # [(0, 0), (s, 0), (s, s), (0, s)]
                [(x, y), (x + s, y), (x + s, y + s), (x, y + s)],
            )
            # hill.body.position = (x, y)
            tower.elasticity = 0.9
            tower.friction = 0.0
            tower.filter = pymunk.ShapeFilter(
                group=CAT_TOWER, categories=CAT_TOWER,
                mask=pymunk.ShapeFilter.ALL_MASKS() ^ CAT_ARROW
            )
            towers.append(tower)

            cell = arcade.Sprite(
                join(BASE_DIR, 'objects/images/Fortress.png'),
                scale=s / 128,
                center_x=x + s // 2,
                center_y=y + s // 2,
            )
            self.game.ui_manager.scene.add_sprite(SPRITE_LIST_STATIC, cell)
        self.space.add(*towers)
        return towers

    def _create_gate(self):
        s = self.params.tower_size
        terrain_w = self.params.width // self.params.cell_size
        terrain_h = self.params.height // self.params.cell_size
        gate = None
        while gate is None:
            x = int(random() * terrain_w)
            y = int(random() * terrain_h)
            if (x, y) in zip(*self.hill_indices):
                continue

            x *= self.params.cell_size
            y *= self.params.cell_size
            gate = pymunk.Poly(
                self.space.static_body,
                [(x, y), (x + s, y), (x + s, y + s), (x, y + s)],
            )
            gate.elasticity = 0.9
            gate.friction = 0.0
            gate.filter = pymunk.ShapeFilter(mask=0)
            self.space.add(gate)

            cell = arcade.Sprite(
                ':resources:images/tiles/lockYellow.png',
                scale=s / 128,
                center_x=x + s // 2,
                center_y=y + s // 2,
            )
            self.game.ui_manager.scene.add_sprite(SPRITE_LIST_STATIC, cell)
        return gate

    @staticmethod
    def _discretize_terrain(t):
        t_hill = 0.5
        t_slope = 0.3
        t_ground = -0.3
        t_sand = -0.5
        t_grass = -0.6

        hills = np.where(t >= t_hill)
        slopes = np.where((t >= t_slope) & (t < t_hill))
        ground = np.where((t >= t_ground) & (t < t_slope))
        sand = np.where((t >= t_sand) & (t < t_ground))
        grass = np.where((t >= t_grass) & (t < t_sand))
        water = np.where((t < t_grass))

        return hills, slopes, ground, sand, grass, water


def generate_perlin_noise_2d(shape, res):
    # Make sure that the shape and resolution are compatible.
    old_shape = list(shape)
    new_shape = []
    for i in range(len(shape)):
        new_shape.append(((shape[i] // res[i]) + 1) * res[i])
    shape = new_shape

    # Perlin Noise
    def f(t):
        return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0: res[0]: delta[0], 0: res[1]: delta[1]].transpose(1, 2, 0) % 1
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

    # Crop to the required shape.
    noise = noise[:old_shape[0], :old_shape[1]]
    return noise
