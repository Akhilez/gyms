import copy
from typing import Tuple, List
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

    @state.setter
    def state(self, state):
        self.board, self.mens = state

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

        if self.is_phase_1():
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
        self.board, self.mens = self.get_empty_state()
        self.turn = 1
        self.done = False

    def render(self, mode='human'):
        s = []
        for x in self.board:
            if x == 0:
                s.append('•')
            elif x == 1:
                s.append('X')
            else:
                s.append('O')
        print(f"""
{s[0]}-----{s[1]}-----{s[2]}
| {s[8]}---{s[9]}---{s[10]} |
| | {s[16]}-{s[17]}-{s[18]} | |
{s[7]}-{s[15]}-{s[23]}   {s[19]}-{s[11]}-{s[3]}
| | {s[22]}-{s[21]}-{s[20]} | |
| {s[14]}---{s[13]}---{s[12]} |
{s[6]}-----{s[5]}-----{s[4]}
""")
        print(self.mens[1:])
        print(f'Turn: {self.turn}')

    def get_legal_actions(self):
        return self.get_legal_actions_(self.state, self.turn)

    def is_phase_1(self):
        return self.is_phase_1_(self.state, self.turn)

    @staticmethod
    def get_empty_state():
        return np.zeros(24), [None, [9, 0], [9, 0]]

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
        if NineMensMorrisEnvV2.is_phase_1_(state, turn):  # Phase 1
            if state[0][action[0]] != 0:
                return 'position_not_empty'
        else:
            if state[0][action[0]] != turn:
                return 'position_invalid'
            moved = moved_positions[action[0]][action[1]]
            if moved is None or state[0][moved] != 0:
                return 'illegal_move'
        if action[2] is not None:
            if state[0][action[2]] != -turn or (
                    len(state[0][state[0] == -turn]) > 3 and NineMensMorrisEnvV2.has_killed(state, action[2])):
                return 'illegal kill'

    @staticmethod
    def is_phase_1_(state, turn):
        return state[1][turn][0] > 0

    @staticmethod
    def is_done(state):
        board = state[0]
        mens = state[1]

        p = 1
        n = -1

        if mens[n][1] == 7 and len(board[board == n]) == 2:
            return p
        if mens[p][1] == 7 and len(board[board == p]) == 2:
            return n

        if not NineMensMorrisEnvV2.is_phase_1_(state, p):
            if not NineMensMorrisEnvV2.is_able_to_move(board, p):
                return n
        if not NineMensMorrisEnvV2.is_phase_1_(state, n):
            if not NineMensMorrisEnvV2.is_able_to_move(board, n):
                return p

        return 0

    @staticmethod
    def is_able_to_move(board, turn):
        positions = np.nonzero(board == turn)[0]
        for position in positions:
            moved_position = moved_positions[position]
            if any([board[i] == 0 for i in moved_position if i is not None]):
                return True
        return False

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
        opponents = NineMensMorrisEnvV2.get_killable_positions(state, turn)
        if NineMensMorrisEnvV2.is_phase_1_(state, turn):  # Phase 1
            actions = np.nonzero(board == 0)[0]
            for action in actions:
                state_ = copy.deepcopy(state)
                state_[0][action] = turn
                has_killed = NineMensMorrisEnvV2.has_killed(state_, action)
                all_actions.append([action, None, has_killed])
            return all_actions, opponents

        for pos in np.nonzero(board == turn)[0]:
            moves = []
            kills = []
            for i in range(4):
                moved = moved_positions[pos][i]
                if moved is not None and board[moved] == 0:
                    state_ = copy.deepcopy(state)
                    state_[0][pos] = 0
                    state_[0][moved] = turn
                    has_killed = NineMensMorrisEnvV2.has_killed(state_, moved)
                    moves.append(i)
                    kills.append(has_killed)
            if len(moves) > 0:
                all_actions.append([pos, moves, kills])
        return all_actions, opponents

    @staticmethod
    def get_killable_positions(state, turn):
        all_opponents = np.nonzero(state[0] == -turn)[0]
        killable_opponents = []
        for opponent in all_opponents:
            if not NineMensMorrisEnvV2.has_killed(state, opponent):
                killable_opponents.append(opponent)
        return np.array(killable_opponents)

    @staticmethod
    def flatten_actions(actions: Tuple[List[Tuple], List[int]]):
        # Actions: [(position, [move1, move1], [bool, bool]),]
        flattened_actions = []
        for action_tup in actions[0]:
            if action_tup[1] is not None and len(action_tup[1]) > 0:  # If moves exist
                assert len(action_tup[1]) == len(action_tup[2]), "Moves and kill booleans must be of same length"
                for i in range(len(action_tup[1])):  # For each move
                    if not action_tup[2][i]:  # If not killed
                        flattened_actions.append((action_tup[0], action_tup[1][i], None))
                    elif len(actions[1]) > 0:  # If killed, then add all kill moves
                        for kill in actions[1]:
                            flattened_actions.append((action_tup[0], action_tup[1][i], kill))
            else:
                if action_tup[2] and len(actions[1]) > 0:
                    for kill in actions[1]:
                        flattened_actions.append((action_tup[0], None, kill))
                else:
                    flattened_actions.append((action_tup[0], None, None))
        return flattened_actions
