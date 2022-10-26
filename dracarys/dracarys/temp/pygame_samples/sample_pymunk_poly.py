"""This is an example on how custom collision filters work.
"""
__docformat__ = "reStructuredText"

import sys

import pygame

import pymunk
import pymunk.autogeometry
import pymunk.pygame_util
from pymunk import ShapeFilter


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = 0, 0

    """
    Just drawing a polygon
    """
    s = 100
    rect = pymunk.Poly(
        space.static_body,
        vertices=[(0, 0), (s, 0), (s, s), (0, s)],
    )
    rect.body.position = (50, 50)
    space.add(rect)

    point = space.point_query(point=(55, 55), max_distance=0, shape_filter=ShapeFilter())
    print(point)

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    pymunk.pygame_util.positive_y_is_up = False

    fps = 60
    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and (event.key in [pygame.K_ESCAPE, pygame.K_q])
            ):
                sys.exit(0)

        space.step(1.0 / fps)

        screen.fill(pygame.Color("white"))
        space.debug_draw(draw_options)
        pygame.display.flip()

        clock.tick(fps)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    sys.exit(main())
