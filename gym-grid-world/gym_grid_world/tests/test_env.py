from gym_grid_world.envs.grid_world_env import GridWorldEnv

env = GridWorldEnv(size=4, mode='static')

env.reset()
env.render()

_, _, done, _ = env.step(0)
print(done)
env.render()

_, _, done, _ = env.step(3)
env.render()
print(done)


_, _, done, _ = env.step(0)
env.render()
print(done)

