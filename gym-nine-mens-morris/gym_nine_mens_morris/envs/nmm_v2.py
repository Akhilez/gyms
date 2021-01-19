import copy

import gym
import numpy as np

moved_positions = [
    [None, None, 1, 7],
    [0, None, 2, 9],
    [1, None, None, 3],
    [11, 2, None, 4],
    [5, 3, None, None],
    [6, 13, 4, None],
    [None, 7, 5, None],  # 6
    [None, 0, 15, 6],
    [None, None, 9, 15],  # 8
    [8, 1, 10, 17],
    [9, None, None, 11],  # 10
    [19, 10, 3, 12],
    [13, 11, None, None],
    [14, 21, 12, 5],
    [None, 15, 13, None],
    [7, 8, 23, 14],
    [None, None, 17, 23],  # 16
    [16, 9, 18, None],  # 17
    [17, None, None, 19],  # 18
    [None, 18, 11, 20],  # 19
    [21, 19, None, None],  # 20
    [22, None, 20, 13],  # 21
    [None, 23, 21, None],  # 22
    [15, 16, None, 22],  # 23
]

alignments = np.array([
    # all rows
    [0, 1, 2],
    [8, 9, 10],
    [16, 17, 18],
    [7, 15, 23],
    [19, 11, 3],
    [22, 21, 20],
    [14, 13, 12],
    [4, 5, 6],

    # All cols
    [6, 7, 0],
    [14, 15, 8],
    [22, 23, 16],
    [5, 13, 21],
    [1, 9, 17],
    [18, 19, 20],
    [10, 11, 12],
    [2, 3, 4]
])


class NineMensMorrisEnvV2(gym.Env):
    metadata = {'render.modes': ['human']}
    reward_range = (-100, 100)
    spec = None

    # Set these in ALL subclasses
    action_space = gym.spaces.Discrete(120)  # (24 * 4) + 24
    observation_space = gym.spaces.Tuple((gym.spaces.Discrete(24), gym.spaces.MultiDiscrete([3, 2])))

    def __init__(self):
        self.turn = None
        self.board = None
        self.mens = None
        self.done = None
        self.winner = None

    @property
    def state(self):
        return self.board, self.mens

    def step(self, action: tuple):
        """
        0. If is done, return
        1. Check phase 1 or 2.
        2. If illegal action, you lose.
        3. If phase 1, set state[action] = turn
        4. If phase 2, move and kill
        :param action: a tuple of shapes ((4), (1), (4))
        :return: state, reward, done, info
        """
        self.winner = self.is_done(self.state)
        self.done = bool(self.winner)
        if self.done:
            return self.state, 100 * self.winner, self.done, {'already_done': True}

        is_illegal_msg = self.is_illegal(self.state, self.turn, action)
        if is_illegal_msg:
            self.done = True
            self.winner = -self.turn
            return self.state, -100, self.done, {is_illegal_msg: True}

        is_phase_1 = self.mens[self.turn][0] > 0
        if is_phase_1:
            self.board[action[0]] = self.turn
            target = action[0]
            self.mens[self.turn][0] -= 1
        else:
            self.board[action[0]] = 0
            target = moved_positions[action[0]][action[1]]
            self.board[target] = self.turn

        has_killed = self.has_killed(self.state, target)
        if has_killed:
            self.board[action[2]] = 0
            self.mens[-self.turn][1] += 1

        self.winner = self.is_done(self.state)
        self.done = bool(self.winner)
        reward = 100 * self.winner if self.done else -0.1
        self.turn *= -1
        return self.state, reward, self.done, {}

    def reset(self):
        self.board = np.zeros(24)
        self.mens = [None, [9, 0], [9, 0]]
        self.turn = 1
        self.done = False

    def render(self, mode='human'):
        print(self.board)
        print(self.mens[1:])
        print(f'Turn: {self.turn}')

    def get_legal_actions(self):
        return self.get_legal_actions_(self.state, self.turn)

    @staticmethod
    def is_illegal(state, turn, action):
        """
        1. If phase 1, check if position is empty
        2. if phase 2
            a. check if position is turn's
            b. check if moved position is out of bounds
            c. check if moved position is occupied
        3. if kill is given, check if that position is -turn's
        """
        if state[1][turn][0] > 0:  # Phase 1
            if state[0][action[0]] != 0:
                return 'position_not_empty'
        else:
            if state[0][action[0]] != turn:
                return 'position_invalid'
            moved = moved_positions[action[0]][action[1]]
            if moved is None or state[0][moved] != 0:
                return 'illegal_move'
        if action[2] is not None:
            if state[0][action[2]] != -turn:
                return 'illegal kill'

    @staticmethod
    def is_done(state):
        board = state[0]
        mens = state[1]

        p = 1
        n = -1

        if mens[n][1] == 9 and len(board[board == n]) == 0:
            return p
        if mens[p][1] == 9 and len(board[board == p]) == 0:
            return n
        return 0

    @staticmethod
    def has_killed(state, recent_move):
        sum_ = state[0][recent_move] * 3
        for alignment in alignments:
            if recent_move in alignment and sum(state[0][alignment]) == sum_:
                return True
        return False

    @staticmethod
    def get_legal_actions_(state, turn):
        all_actions = []
        board = state[0]
        opponents = np.nonzero(board == -turn)[0]
        if state[1][turn][0] > 0:  # Phase 1
            actions = np.nonzero(board == 0)[0]
            for action in actions:
                state_ = copy.deepcopy(state)
                state_[0][action] = turn
                has_killed = NineMensMorrisEnvV2.has_killed(state_, action)
                all_actions.append([action, None, has_killed])
            return all_actions, opponents

        for pos in np.nonzero(board == turn)[0]:
            for i in range(4):
                moved = moved_positions[pos][i]
                if moved is not None and board[moved] == 0:
                    state_ = copy.deepcopy(state)
                    state_[0][pos] = 0
                    state_[0][moved] = turn
                    has_killed = NineMensMorrisEnvV2.has_killed(state_, moved)
                    all_actions.append([pos, i, has_killed])
        return all_actions, opponents