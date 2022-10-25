import sys

import arcade
import numpy as np
import pygame
import pymunk


def run():
    pygame.init()
    _display = pygame.display.set_mode(
        (600, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF
    )


    pygame.display.set_caption("Joints. Just wait and the L will tip over")
    clock = pygame.time.Clock()

    window = arcade.Window(500, 500, visible=False)

    space = pymunk.Space()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        space.step(1 / 50.0)
        clock.tick(50)


        window.clear()
        arcade.draw_rectangle_filled(50, 50, 50, 50, color=arcade.color.AMAZON)
        image = arcade.get_image(0, 0, *window.get_size())
        image = np.asarray(image)  # shape (h, w, 4) (RGBA)
        image = image[:, :, :3]  # shape (h, w, 3)  Got rid of alpha channel


        _display.blit(pygame.surfarray.make_surface(image), (0, 0))
        pygame.display.update()

    pygame.quit()


