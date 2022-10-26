"""This is an example on how custom collision filters work.
"""
__docformat__ = "reStructuredText"

import sys

import pygame

import pymunk
import pymunk.autogeometry
import pymunk.pygame_util


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = 0, 980

    """
    Collision map:
    type, category, category mask (eligible collisions)

    light: 1, (3, 4)
    heavy: 2, (4)
    
    soft: 3, (1)
    hard: 4, (1, 2)
    """

    hard = pymunk.Segment(space.static_body, (50, 550), (550, 550), 5)
    hard.collision_type = 1
    hard.filter = pymunk.ShapeFilter(categories=4)#, mask=1 | 2)
    space.add(hard)

    soft = pymunk.Segment(space.static_body, (250, 350), (550, 250), 5)
    soft.collision_type = 1
    soft.filter = pymunk.ShapeFilter(categories=3)#, mask=1)
    space.add(soft)

    heavy = pymunk.Circle(pymunk.Body(),  radius=15)
    heavy.mass = 1
    heavy.body.position = (400, 100)
    heavy.filter = pymunk.ShapeFilter(categories=2, mask=pymunk.ShapeFilter.ALL_MASKS() ^ 3)#4)
    space.add(heavy.body, heavy)

    light = pymunk.Circle(pymunk.Body(), radius=15)
    light.mass = 1
    light.body.position = (250, 100)
    light.filter = pymunk.ShapeFilter(categories=1, mask=3 | 4)
    space.add(light.body, light)

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
