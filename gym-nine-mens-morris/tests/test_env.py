from gym_nine_mens_morris.envs import NineMensMorrisEnv

env = NineMensMorrisEnv()

state = env.reset()
reward = env.step(4)

print(state)
print(reward)

