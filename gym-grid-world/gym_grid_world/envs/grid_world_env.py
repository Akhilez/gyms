import gym
import numpy as np

from gym_grid_world.envs.simple_grid_world_env.GridWorld import Gridworld


class GridWorldEnv(gym.Env):
    def __init__(self, size, mode="static"):
        self.size = size
        self.mode = mode
        self.done = False
        self.won = False
        self.env: Gridworld = None
        self.actions = ["l", "u", "r", "d"]

    @property
    def state(self):
        return self.env.board.render_np()

    @state.setter
    def state(self, positions: dict):
        self.env.board.components["Player"].pos = positions["player"]  # Row, Column
        self.env.board.components["Goal"].pos = positions["win"]
        self.env.board.components["Pit"].pos = positions["pit"]
        self.env.board.components["Wall"].pos = positions["wall"]

    def step(self, action: int):
        self.env.makeMove(self.actions[action])
        reward = self.env.reward()
        self.done = reward ** 2 == 100
        self.won = reward == 10
        return self.env.board.render_np(), reward, self.done, {}

    def reset(self):
        self.env = Gridworld(size=self.size, mode=self.mode)
        self.done = False
        self.won = False
        return self.state

    def render(self, mode="human"):
        print()
        print(self.env.board.render())
        print()

    @staticmethod
    def get_legal_actions():
        return np.arange(4)

    def get_positions(self) -> dict:
        return self.get_positions_(self.state)

    def set_state(self, state: np.ndarray):
        positions = self.get_positions_(state)
        self.state = positions

    @staticmethod
    def get_positions_(state: np.ndarray) -> dict:
        player, win, pit, wall = [
            np.array(np.nonzero(s == 1)).flatten().tolist() for s in state
        ]
        return {"player": player, "win": win, "pit": pit, "wall": wall}

    @staticmethod
    def is_done(state: np.ndarray) -> bool:
        positions = GridWorldEnv.get_positions_(state)
        player = positions["player"]
        return player == positions["win"] or player == positions["pit"]

    @staticmethod
    def has_won(state: np.ndarray) -> bool:
        positions = GridWorldEnv.get_positions_(state)
        player = positions["player"]
        return player == positions["win"]
