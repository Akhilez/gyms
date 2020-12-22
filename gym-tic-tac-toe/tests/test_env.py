from gym_tic_tac_toe.envs import TicTacToeEnv

env = TicTacToeEnv()

state = env.reset()
reward = env.step(4)

print(state)
print(reward)

