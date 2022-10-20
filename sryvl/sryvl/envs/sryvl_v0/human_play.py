import pygame
from skimage.transform import resize
from sryvl.envs.sryvl_v0.env import SrYvlLvl0Env
import numpy as np


def main():
    key_map = [
        pygame.K_r,
        pygame.K_a,
        pygame.K_w,
        pygame.K_d,
        pygame.K_s,
        pygame.K_e,
        pygame.K_q,
        pygame.K_c,
        pygame.K_f,
        pygame.K_g,
    ]

    pygame.init()
    window = pygame.display.set_mode((63 * 5, 63 * 5))
    clock = pygame.time.Clock()

    environment = SrYvlLvl0Env()
    run = True
    while run:
        # set game speed to 3 fps
        clock.tick(2)

        action = 0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                for i, key in enumerate(key_map):
                    if event.key == key:
                        action = i
            elif event.type == pygame.QUIT:
                run = False

        obs, reward, done, info = environment.step(action)
        obs = np.moveaxis(obs, 0, -1)
        obs = resize(obs, (63 * 5, 63 * 5), anti_aliasing=False)
        obs = (obs * 255).astype(int)
        obs = obs.transpose((1, 0, 2))
        if done:
            run = False

        window.blit(pygame.surfarray.make_surface(obs), (0, 0))
        pygame.display.update()

    pygame.quit()
    print(environment.stats_agg)


if __name__ == '__main__':
    print("""
Controls:
w: up
a: left
s: down
d: right
e: eat
q: kill
c: store
f: place plant
g: place poison
""")
    main()
