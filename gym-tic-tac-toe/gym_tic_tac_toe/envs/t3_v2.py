import gym
import numpy as np


class TicTacToeEnvV2(gym.Env):
    metadata = {'render.modes': ['human']}
    reward_range = (-10, 10)
    spec = None

    # Set these in ALL subclasses
    action_space = gym.spaces.Discrete(1)
    observation_space = gym.spaces.Discrete(9)

    def __init__(self):
        self.turn = None
        self.state = None
        self.done = None
        self.winner = None

    def step(self, action: int):
        if self.state[action] != 0:
            self.done = True
            reward = -10
            return self.state, reward, self.done, {'illegal_action': True}

        self.state[action] = self.turn
        is_winner = self._is_winner()
        reward = 10 if is_winner else -1
        if is_winner:
            self.winner = self.turn
        self.done = is_winner or self._is_done()
        self.turn *= -1
        return self.state, reward, self.done, {}

    def reset(self):
        self.state = np.zeros(9)
        self.turn = 1
        self.done = False

    def render(self, mode='human'):
        s = self.state.reshape(3, 3)
        for i in range(3):
            for j in range(3):
                piece = s[i][j]
                if piece == 1:
                    piece = 'X'
                elif piece == -1:
                    piece = 'O'
                else:
                    piece = '.'
                print(piece, end=' ')
            print()
        print(f'Next: {self.turn}')

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def get_legal_actions(self):
        return np.nonzero(self.state == 0)[0]

    def _is_winner(self):
        s = self.state.reshape((3, 3))
        winner = np.ones(3) * 3 * self.turn

        # All rows
        if any(np.sum(s, 1) == winner):
            return True

        if any(np.sum(s, 0) == winner):
            return True

        d1 = np.array((0, 4, 8))
        d2 = np.array((2, 4, 6))

        if np.sum(self.state[d1]) == winner[0]:
            return True

        if np.sum(self.state[d2]) == winner[0]:
            return True

        return False

    def _is_done(self):
        return len(np.nonzero(self.state == 0)[0]) == 0
