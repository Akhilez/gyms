from gym.envs.registration import register

register(
    id='grid-world-v0',
    entry_point='gym_grid_world.envs:GridWorldEnv',
)
