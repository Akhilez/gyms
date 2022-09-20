from typing import Tuple, List
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np

np.set_printoptions(linewidth=10000, threshold=np.inf)

NOTHING = 0
AGENT = 1
FOOD = 2
TERRAIN = 3
BOUNDARY = 4

ACTION_NONE = 0
ACTION_LEFT = 1
ACTION_UP = 2
ACTION_RIGHT = 3
ACTION_DOWN = 4

POSITION_OFFSETS = {
    ACTION_NONE: (0, 0),
    ACTION_LEFT: (0, -1),
    ACTION_UP: (-1, 0),
    ACTION_RIGHT: (0, +1),
    ACTION_DOWN: (1, 0),
}


class Food:
    def __init__(self, position, expiry_period):
        self.age = 0
        self.expired = False
        self.position = position
        self.expiry_period = expiry_period

    def step(self):
        self.age += 1
        self.expired = self.age >= self.expiry_period


class SrYvlLvl0Env(Env):
    metadata = {'render.modes': ['human']}
    reward_range = (-np.inf, np.inf)

    # Set these in ALL subclasses
    action_space = Discrete(5)
    observation_space = Box(low=0, high=4, shape=(5, 5))

    def __init__(
            self,
            world_size=50,
            max_agent_size=2,
            food_growth_density=2,
            food_growth_radius=5,
            food_expiry_period=500,
            initial_food_density=0.01,
            agent_growth_rate=0.01,
            shrink_rate_min=0.0005,
            shrink_rate_max=0.001,
            movement_shrink_penalty=5,
            observation_radius=5,
            size_threshold_to_jump=1.5,
    ):
        super(SrYvlLvl0Env, self).__init__()

        self.world_size = world_size
        self.max_agent_size = max_agent_size
        self.food_growth_density = food_growth_density
        self.food_growth_radius = food_growth_radius
        self.food_expiry_period = food_expiry_period
        self.initial_food_density = initial_food_density
        self.agent_growth_rate = agent_growth_rate
        self.shrink_rate_min = shrink_rate_min
        self.shrink_rate_max = shrink_rate_max
        self.movement_shrink_penalty = movement_shrink_penalty
        self.observation_radius = observation_radius
        self.size_threshold_to_jump = size_threshold_to_jump

        self.agent_size = 1
        self.agent_position = [0, 0]
        self.foods: List[Food] = []
        self.terrain: List[Tuple[int, int]] = []
        self.world = np.array([])
        self.boundary_indices: List[Tuple[int, int]] = []

        self.legal_actions = np.ones(self.action_space.n)
        self.done = False

        self.reset()

    def render(self, mode='human'):
        if mode == 'world_console':
            print(self.agent_size)

            state = '\n'.join([''.join(i) for i in self.world.astype(str)])
            state = state.replace('4', '□')  # Boundary
            state = state.replace('3', '■')  # Terrain
            state = state.replace('2', '•')  # Food
            state = state.replace('1', '🔺')  # Player
            state = state.replace('0', ' ')  # Nothing
            state = state.replace('.', '')

            print(state)

        elif mode == 'observable_console':
            print(self.agent_size)

            state = '\n'.join([' '.join(i) for i in self.observe().astype(str)])
            state = state.replace('4', '□')  # Boundary
            state = state.replace('3', '■')  # Terrain
            state = state.replace('2', '•')  # Food
            state = state.replace('1', '🔺')  # Player
            state = state.replace('0', ' ')  # Nothing
            state = state.replace('.', '')

            print(state)

        else:
            print(self.agent_size)
            print(self.observe())

    def step(self, action: int) -> Tuple[np.array, float, bool, dict]:
        """
        0 = no action
        1 = left
        2 = up
        3 = right
        4 = down

        - check if action is legal or not.
        - no action = lose energy according to idle shrink rate
        - action direction:
            - lose energy
            - If there's food:
                - gain energy
                - mark the food as eaten
            - move agent's location
        - Grow food
        - check if done -- if agent's health == 0
        - reward = 1
        - Find the legal actions
        - Redraw world
        """

        if self.legal_actions[action] == 0:  # Illegal action.
            self.legal_actions = np.zeros(self.action_space.n)
            self.done = True
            return self.observe(), 0, self.done, {}

        y, x = POSITION_OFFSETS[action]
        self.agent_position[0] += y
        self.agent_position[1] += x

        [food.step() for food in self.foods]
        self._clear_expired_foods()
        self._grow_agent()
        self._grow_more_food()

        shrink_rate_movement = self._get_shrink_rate_movement()
        shrink_rate_movement *= 1 if action == ACTION_NONE else self.movement_shrink_penalty
        self.agent_size -= shrink_rate_movement

        if self.agent_size <= 0:
            self.done = True

        self.legal_actions = self._find_legal_actions()
        self.draw_env()

        return self.observe(), 1.0, self.done, {}

    def reset(self, *_args, **_kwargs) -> None:
        self.agent_size = 1

        side = self.world_size + (self.observation_radius * 2)
        self.world = np.zeros((side, side))

        food_positions = self.get_initial_food_positions(side, self.initial_food_density)
        self.fill_indices(self.world, food_positions, FOOD)

        self.terrain = self.make_terrain(side)
        self.fill_indices(self.world, self.terrain, TERRAIN)

        self.boundary_indices = self.make_boundary(side, self.observation_radius)
        self.fill_indices(self.world, self.boundary_indices, BOUNDARY)

        self.foods = [
            Food(pos, self.food_expiry_period)
            for pos in self.find_indices(self.world, FOOD)
        ]

        self.agent_position = self._get_agent_initial_position()
        self.fill_indices(self.world, [self.agent_position], AGENT)

        self.legal_actions = np.ones(self.action_space.n)
        self.done = False

        return self.observe()

    def observe(self) -> np.array:
        r = self.observation_radius
        y = self.agent_position[0]
        x = self.agent_position[1]
        x0, y0, x1, y1 = x - r, y - r, x + r + 1, y + r + 1
        return self.world[y0: y1, x0: x1]

    def sample_action(self):
        mask = self.legal_actions.astype(float)
        assert sum(mask) > 0, "No legal actions"
        return np.random.choice(len(mask), p=mask / mask.sum())

    def draw_env(self) -> np.array:
        side = self.world_size + (self.observation_radius * 2)
        self.world = np.ones((side, side)) * NOTHING
        self.fill_indices(self.world, [f.position for f in self.foods], FOOD)
        self.fill_indices(self.world, self.terrain, TERRAIN)
        self.fill_indices(self.world, self.boundary_indices, BOUNDARY)
        self.fill_indices(self.world, [self.agent_position], AGENT)

    def _grow_more_food(self):
        more_foods = []
        for food in self.foods:
            growth_window = self._get_food_growth_window(food)
            if not self._enough_food_already_exists_nearby(growth_window):
                chance = food.age / (self.food_expiry_period * 2) > np.random.rand()
                if chance:
                    more_foods.append(
                        Food(
                            self._get_random_position_nearby(growth_window),
                            self.food_expiry_period,
                        )
                    )
        self.foods.extend(more_foods)

    def _enough_food_already_exists_nearby(self, growth_window):
        """num_food in radius < food_growth_density"""
        num_food = len(SrYvlLvl0Env.find_indices(growth_window, FOOD)) - 1
        return num_food < self.food_growth_density

    def _get_food_growth_window(self, food):
        y = food.position[0]
        x = food.position[1]

        x0 = max(0, x - self.food_growth_radius)
        y0 = max(0, y - self.food_growth_radius)
        x1 = min(len(self.world), x + self.food_growth_radius + 1)
        y1 = min(len(self.world), y + self.food_growth_radius + 1)

        return self.world[y0:y1, x0:x1]

    @staticmethod
    def _get_random_position_nearby(growth_window):
        empty_positions = SrYvlLvl0Env.find_indices(growth_window, NOTHING)
        return empty_positions[np.random.choice(len(empty_positions))]

    def _grow_agent(self):
        new_size = self.agent_size + self.agent_growth_rate
        if new_size <= self.max_agent_size:
            for i, food in enumerate(self.foods):
                if food.position[0] == self.agent_position[0] and food.position[1] == self.agent_position[1]:
                    self.agent_size = new_size
                    del self.foods[i]

    def _clear_expired_foods(self):
        self.foods = [food for food in self.foods if food.position is not None]
        self.fill_indices(self.world, self.find_indices(self.world, FOOD), NOTHING)

    def _find_legal_actions(self):
        """
        - If agent's health is 0, all actions are illegal.
        - If agent has a BOUNDARY in a direction d, then d is illegal.
        - If agent has a terrain in a direction d:
            - if the agent size < threshold, then d is illegal
        """
        if self.agent_size <= 0:
            return np.zeros(self.action_space.n)

        nothing, left, up, right, down = 1, 1, 1, 1, 1

        y = self.agent_position[0]
        x = self.agent_position[1]

        if self.world[y, x - 1] == BOUNDARY:
            left = 0
        if self.world[y - 1, x] == BOUNDARY:
            up = 0
        if self.world[y, x + 1] == BOUNDARY:
            right = 0
        if self.world[y + 1, x] == BOUNDARY:
            down = 0

        if self.agent_size < self.size_threshold_to_jump:
            if self.world[y, x - 1] == TERRAIN:
                left = 0
            if self.world[y - 1, x] == TERRAIN:
                up = 0
            if self.world[y, x + 1] == TERRAIN:
                right = 0
            if self.world[y + 1, x] == TERRAIN:
                down = 0

        return np.array([nothing, left, up, right, down])

    def _get_shrink_rate_movement(self):
        return (self.shrink_rate_max - self.shrink_rate_min) / self.max_agent_size * self.agent_size + self.shrink_rate_min

    def _get_agent_initial_position(self):
        available_indices = np.array((self.world == NOTHING).nonzero()).T
        return available_indices[np.random.choice(len(available_indices))]

    @staticmethod
    def find_indices(world, category):
        return np.array((world == category).nonzero()).T

    @staticmethod
    def make_terrain(world_size) -> List[Tuple[int, int]]:
        """
        Add perlin noise for terrain, then another layer of perlin noise as nothing.
        """
        # TODO Get perlin noise
        terrain = np.random.random((world_size, world_size))
        terrain = (terrain < 0.1) * TERRAIN
        return np.array((terrain == TERRAIN).nonzero()).T

    @staticmethod
    def make_boundary(world_size, observation_radius) -> List[Tuple[int, int]]:
        # Add boundary padding
        boundary = np.zeros((world_size, world_size))
        boundary[:observation_radius, :] = BOUNDARY
        boundary[-observation_radius:, :] = BOUNDARY
        boundary[:, :observation_radius] = BOUNDARY
        boundary[:, -observation_radius:] = BOUNDARY
        return np.array((boundary == BOUNDARY).nonzero()).T

    @staticmethod
    def get_initial_food_positions(world_size, initial_food_density) -> List[Tuple[int, int]]:
        pos = np.random.random(size=(world_size, world_size))
        pos = pos < initial_food_density
        pos = np.array(pos.nonzero()).T
        return pos

    @staticmethod
    def fill_indices(world, positions, fill):
        for position in positions:
            world[tuple(position)] = fill


def main():
    env = SrYvlLvl0Env(initial_food_density=0.2, world_size=10)
    env.render(mode='world_console')
    for i in range(10):
        env.step(env.sample_action())
        env.render(mode='world_console')


def human_play():
    env = SrYvlLvl0Env(initial_food_density=0.2, world_size=10)
    while not env.done:
        env.render(mode='world_console')
        inp = input('wasde input: ')
        key = 'eawds'
        action = key.index(inp)
        env.step(action)


if __name__ == '__main__':
    human_play()
