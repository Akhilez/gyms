from typing import Tuple, List
from gym import Env
from gym.envs.registration import EnvSpec
from gym.spaces import Discrete, Box
import numpy as np
from functools import reduce
from collections import deque
from sryvl.envs.sryvl_v0.assets import make_obs


np.set_printoptions(linewidth=10000, threshold=np.inf)

NOTHING = 0
AGENT = 1
FOOD = 2
TERRAIN = 3
BOUNDARY = 4
POISON = 5

ACTION_NONE = 0
ACTION_LEFT = 1
ACTION_UP = 2
ACTION_RIGHT = 3
ACTION_DOWN = 4
ACTION_EAT = 5
ACTION_KILL = 6
ACTION_STORE = 7
# ACTION_PLANT = 8

POSITION_OFFSETS = {
    ACTION_NONE: (0, 0),
    ACTION_LEFT: (0, -1),
    ACTION_UP: (-1, 0),
    ACTION_RIGHT: (0, +1),
    ACTION_DOWN: (1, 0),
    ACTION_EAT: (0, 0),
    ACTION_KILL: (0, 0),
    ACTION_STORE: (0, 0),
}


class Food:
    def __init__(self, position, expiry_period, is_poison):
        self.age = 0
        self.expired = False
        self.position = position
        self.expiry_period = expiry_period
        self.is_poison = is_poison

    def step(self):
        self.age += 1
        self.expired = self.age >= self.expiry_period


class SrYvlLvl0Env(Env):
    metadata = {
        "render_modes": [
            "human",
            "ansi",
            "rgb_array",
            "flattened_planes",
        ]
    }
    reward_range = (1, 1)
    action_space = Discrete(6)
    observation_space = Box(low=0, high=255, shape=(3, 7*9, 7*9), dtype=np.uint8)
    # observation_space = Box(low=0, high=4, shape=(49,), dtype=int)
    # observation_space = Box(low=0, high=2 * 20, shape=(294,), dtype=np.float64)
    spec = EnvSpec(
        id='sryvl-v0',
        entry_point='sryvl.envs.sryvl_v0.sryvl:SrYvlLvl0Env',
        max_episode_steps=30_000,
    )

    def __init__(
        self,
        world_size=20,
        max_agent_size=2,
        food_growth_density=3,
        food_growth_radius=2,
        food_expiry_period=50,
        initial_food_density=0.2,
        poison_fraction=0.5,
        growth_rate_min=0.01,
        growth_rate_max=0.1,
        shrink_rate_min=0.009,
        shrink_rate_max=0.01,
        movement_shrink_penalty=1.05,
        observation_radius=3,
        size_threshold_to_jump=1.5,
        terrain_resolution=8,
        terrain_intensity=0.8,
        max_inventory=5,
    ):
        super(SrYvlLvl0Env, self).__init__()

        self.world_size = world_size
        self.max_agent_size = max_agent_size
        self.food_growth_density = food_growth_density
        self.food_growth_radius = food_growth_radius
        self.food_expiry_period = food_expiry_period
        self.initial_food_density = initial_food_density
        self.poison_fraction = poison_fraction
        self.growth_rate_min = growth_rate_min
        self.growth_rate_max = growth_rate_max
        self.shrink_rate_min = shrink_rate_min
        self.shrink_rate_max = shrink_rate_max
        self.movement_shrink_penalty = movement_shrink_penalty
        self.observation_radius = observation_radius
        self.size_threshold_to_jump = size_threshold_to_jump
        self.terrain_resolution = terrain_resolution
        self.terrain_intensity = terrain_intensity
        self.max_inventory = max_inventory

        self.agent_size = 1
        self.agent_position = [0, 0]
        self.foods: List[Food] = []
        self.plant_inventory = 0
        self.poison_inventory = 0
        self.terrain: List[Tuple[int, int]] = []
        self.world = np.array([])
        self.boundary_indices: List[Tuple[int, int]] = []
        self._distances_from_center = np.array([])

        self.legal_actions = np.ones(self.action_space.n)
        self.done = False
        self.agent_history = deque(maxlen=world_size)

        self.stats_agg = {}

        self.reset()

    def render(self, mode="human"):
        assert mode in self.metadata['render_modes']

        if mode in ("human", 'ansi'):
            print(self.agent_size)
            world = self.world.copy()
            world[tuple(self.agent_position)] = AGENT

            state = "\n".join([" ".join(i) for i in world.astype(str)])
            state = state.replace("4", "□")  # Boundary
            state = state.replace("3", "■")  # Terrain
            state = state.replace("2", "•")  # Food
            state = state.replace("1", "🔺")  # Player
            state = state.replace("0", " ")  # Nothing
            state = state.replace("5", "◦")  # Poison
            state = state.replace(".", "")

            print(state)
        else:
            """
            planes:
            0: Boundary
            1: Terrain
            2: Food Ages
            3: Poison Ages
            4: Player Health
            5: Dist b/w center of the map to each point
            6: Previous path of the player health
            """

            r = self.observation_radius
            y = self.agent_position[0]
            x = self.agent_position[1]
            x0, y0, x1, y1 = x - r, y - r, x + r + 1, y + r + 1
            window = self.world[y0:y1, x0:x1]

            boundary = (window == BOUNDARY) * 1.0
            terrain = self._observe_terrain()[y0:y1, x0:x1]
            food_ages = self._observe_food_ages(is_poison=False)[y0:y1, x0:x1]
            poison_ages = self._observe_food_ages(is_poison=True)[y0:y1, x0:x1]
            player_health = np.zeros_like(window, dtype=float)
            player_health[self.observation_radius, self.observation_radius] = self.agent_size
            distances_from_center = self._distances_from_center[y0:y1, x0:x1]
            history = self._draw_history_map()[y0:y1, x0:x1]

            obs = np.array(
                [
                    boundary,
                    terrain,
                    food_ages,
                    poison_ages,
                    player_health,
                    distances_from_center,
                    history,
                ]
            )
            if mode == "flattened_planes":
                obs = obs.flatten()
            else:  # mode == 'rgb_array':
                obs = make_obs(obs, self.plant_inventory, self.poison_inventory, self.size_threshold_to_jump)
            return obs

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

        self.agent_history.append((tuple(self.agent_position), self.agent_size))

        if self.legal_actions[action] == 0:  # Illegal action == Noop
            action = 0

        y, x = POSITION_OFFSETS[action]
        self.agent_position[0] += y
        self.agent_position[1] += x

        # ----- HEALTH -----
        self._shrink_agent(moved=(x != 0 or y != 0))
        if action == ACTION_EAT:
            self._grow_agent()
        elif action == ACTION_KILL:
            self._kill_food()

        # ----- FOODS ------
        if action == ACTION_STORE:
            self._store_item()
        [food.step() for food in self.foods]
        self.stats_agg['n_foods_expired'].append(sum([1 for food in self.foods if food.expired]))
        self._clear_expired_foods()
        self._grow_more_food()

        self.draw_env()
        self.legal_actions = self._find_legal_actions()
        if sum(self.legal_actions) == 0:
            self.done = True

        self.stats_agg["steps"] += 1
        self.stats_agg['health'].append(self.agent_size)
        self.stats_agg['has_eaten'].append(action == ACTION_EAT)

        return self.observe(), 1.0, self.done, {}

    def reset(self, *_args, **_kwargs) -> None:
        self.agent_size = 1

        side = self.world_size + (self.observation_radius * 2)
        self.world = np.zeros((side, side), dtype=int)

        food_positions = self.get_initial_food_positions(
            side, self.initial_food_density
        )
        self.fill_indices(self.world, food_positions, FOOD)

        self.terrain = self.make_terrain(
            side, self.terrain_resolution, self.terrain_intensity
        )
        self.fill_indices(self.world, self.terrain, TERRAIN)

        self.boundary_indices = self.make_boundary(side, self.observation_radius)
        self.fill_indices(self.world, self.boundary_indices, BOUNDARY)

        self.foods = [
            Food(pos, self.food_expiry_period, np.random.rand() < self.poison_fraction)
            for pos in self.find_indices(self.world, FOOD)
        ]
        for food in self.foods:
            food.age = np.random.randint(self.food_expiry_period)
            if food.is_poison:
                self.world[tuple(food.position)] = POISON

        self.agent_position = self._get_agent_initial_position()

        self.legal_actions = self._find_legal_actions()
        self.done = False
        self.agent_history = []
        self.plant_inventory = 0
        self.poison_inventory = 0
        self._distances_from_center = self._get_distances_from_center(side)

        max_buffer = 500
        self.stats_agg = {
            "steps": 0,
            "food_eaten": 0,
            'poison_eaten': 0,
            "n_foods_available": deque(maxlen=max_buffer),
            "n_foods_expired": deque(maxlen=max_buffer),
            "n_foods_generated": deque(maxlen=max_buffer),
            "has_eaten": deque(maxlen=max_buffer),
            "health": deque(maxlen=max_buffer),
        }

        return self.observe()

    def observe(self) -> np.array:
        return self.render(mode="rgb_array")

    def sample_action(self):
        mask = self.legal_actions.astype(float)
        assert sum(mask) > 0, "No legal actions"
        return np.random.choice(len(mask), p=mask / mask.sum())

    def draw_env(self) -> np.array:
        side = self.world_size + (self.observation_radius * 2)
        self.world = np.ones((side, side), dtype=int) * NOTHING
        self.fill_indices(self.world, [f.position for f in self.foods if not f.is_poison], FOOD)
        self.fill_indices(self.world, [f.position for f in self.foods if f.is_poison], POISON)
        self.fill_indices(self.world, self.terrain, TERRAIN)
        self.fill_indices(self.world, self.boundary_indices, BOUNDARY)

    def _observe_food_ages(self, is_poison: False):
        ages = np.zeros((len(self.world), len(self.world)))
        for food in self.foods:
            if (is_poison and food.is_poison) or (not is_poison and not food.is_poison):
                ages[tuple(food.position)] = food.age / self.food_expiry_period
        return ages

    def _observe_terrain(self):
        terrain = np.zeros((len(self.world), len(self.world)))
        self.fill_indices(terrain, self.terrain, 1)
        return terrain

    def _grow_more_food(self):
        more_foods = []
        for food in self.foods:
            growth_window = self._get_food_growth_window(food)
            # Cannot grow more than the set density
            if not self._enough_food_already_exists_nearby(growth_window):
                # Older plants will have higher probability of growing more plants
                chance = food.age / (self.food_expiry_period**1.5) > np.random.rand()
                if chance:
                    random_position = self._get_random_position_nearby(growth_window)
                    if random_position is not None:
                        # Converting from window indices to world indices
                        random_position[0] += food.position[0] - self.food_growth_radius
                        random_position[1] += food.position[1] - self.food_growth_radius
                        if random_position is not None:
                            more_foods.append(
                                Food(
                                    random_position,
                                    self.food_expiry_period,
                                    food.is_poison,
                                )
                            )
        self.stats_agg['n_foods_generated'].append(len(more_foods))
        self.foods.extend(more_foods)
        self.stats_agg['n_foods_available'].append(len(self.foods))

    def _enough_food_already_exists_nearby(self, growth_window):
        """num_food in radius < food_growth_density"""
        num_food = len(SrYvlLvl0Env.find_indices(growth_window, FOOD)) - 1
        return num_food >= self.food_growth_density

    def _get_food_growth_window(self, food):
        y = food.position[0]
        x = food.position[1]

        x0 = max(0, x - self.food_growth_radius)
        y0 = max(0, y - self.food_growth_radius)
        x1 = min(len(self.world), x + self.food_growth_radius + 1)
        y1 = min(len(self.world), y + self.food_growth_radius + 1)

        return self.world[y0:y1, x0:x1]

    def _draw_history_map(self):
        side = len(self.world)
        history = np.zeros((side, side))
        for position, health in self.agent_history:
            history[tuple(position)] += health
        return history

    @staticmethod
    def _get_random_position_nearby(growth_window):
        empty_positions = SrYvlLvl0Env.find_indices(growth_window, NOTHING)
        if len(empty_positions) > 0:
            return empty_positions[np.random.choice(len(empty_positions))]

    def _grow_agent(self):
        i = [i for i, f in enumerate(self.foods) if tuple(f.position) == tuple(self.agent_position)][0]
        food = self.foods[i]

        delta = self._get_food_yield(food.age)
        if food.is_poison:
            self.agent_size -= delta
            self.stats_agg['poison_eaten'] += 1
        elif self.agent_size + delta <= self.max_agent_size:
            self.agent_size += delta
            self.stats_agg['food_eaten'] += 1
        del self.foods[i]

    def _shrink_agent(self, moved: bool):
        shrink_rate_movement = self._get_shrink_rate_movement()
        shrink_rate_movement *= 1 if moved else self.movement_shrink_penalty
        self.agent_size -= shrink_rate_movement

    def _kill_food(self):
        i = [i for i, f in enumerate(self.foods) if tuple(f.position) == tuple(self.agent_position)][0]
        del self.foods[i]

    def _store_item(self):
        i = [i for i, f in enumerate(self.foods) if tuple(f.position) == tuple(self.agent_position)][0]
        if self.foods[i].is_poison:
            self.poison_inventory += 1
        else:
            self.plant_inventory += 1
        del self.foods[i]

    def _clear_expired_foods(self):
        self.foods = [food for food in self.foods if not food.expired]
        self.fill_indices(self.world, self.find_indices(self.world, FOOD), NOTHING)
        self.fill_indices(self.world, [f.position for f in self.foods], FOOD)

    def _find_legal_actions(self):
        """
        - If agent's health is 0, all actions are illegal.
        - If agent has a BOUNDARY in a direction d, then d is illegal.
        - If agent has a terrain in a direction d:
            - if the agent size < threshold, then d is illegal
        """
        if self.agent_size <= 0:
            return np.zeros(self.action_space.n)

        nothing, left, up, right, down, eat, kill, store = 1, 1, 1, 1, 1, 0, 0, 0

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

        agent_on = self.world[tuple(self.agent_position)]
        # If agent already on terrain (from previous high health), it can move on top of the terrain.
        if agent_on != TERRAIN and self.agent_size < self.size_threshold_to_jump:
            if self.world[y, x - 1] == TERRAIN:
                left = 0
            if self.world[y - 1, x] == TERRAIN:
                up = 0
            if self.world[y, x + 1] == TERRAIN:
                right = 0
            if self.world[y + 1, x] == TERRAIN:
                down = 0

        if agent_on in (FOOD, POISON):
            eat = 1
            kill = 1
            if self.plant_inventory + self.poison_inventory < self.max_inventory:
                store = 1

        return np.array([nothing, left, up, right, down, eat, kill, store])

    def _get_shrink_rate_movement(self):
        """Linearly increasing function b/w min and max. x axis = agent_size."""
        return (
            self.shrink_rate_max - self.shrink_rate_min
        ) / self.max_agent_size * self.agent_size + self.shrink_rate_min

    def _get_food_yield(self, food_age):
        """Linearly increasing function b/w min and max. x axis = food age."""
        return (
            self.growth_rate_max - self.growth_rate_min
       ) / self.food_expiry_period * food_age + self.growth_rate_min

    def _get_agent_initial_position(self):
        available_indices = np.array((self.world == NOTHING).nonzero()).T
        return available_indices[np.random.choice(len(available_indices))]

    @staticmethod
    def _get_distances_from_center(side):
        dist = np.zeros((side, side))
        center = side // 2
        max_distance = np.linalg.norm(np.array([0, 0]) - np.array([center, center]))
        for i in range(side):
            for j in range(side):
                distance = np.linalg.norm(np.array([i, j]) - np.array([center, center]))
                distance /= max_distance
                dist[i, j] = distance
        return dist

    @staticmethod
    def find_indices(world, category):
        return np.array((world == category).nonzero()).T

    @staticmethod
    def make_terrain(
        world_size, terrain_resolution, terrain_intensity
    ) -> List[Tuple[int, int]]:
        """
        Add perlin noise for terrain, then another layer of perlin noise as nothing.
        """

        size = world_size + terrain_resolution - world_size % terrain_resolution
        terrain = generate_perlin_noise_2d(
            shape=(size, size), res=[terrain_resolution, terrain_resolution]
        )
        terrain = terrain[:world_size, :world_size]
        return np.array((terrain > (1 - terrain_intensity)).nonzero()).T

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
    def get_initial_food_positions(
        world_size, initial_food_density
    ) -> List[Tuple[int, int]]:
        pos = np.random.random(size=(world_size, world_size))
        pos = pos < initial_food_density
        pos = np.array(pos.nonzero()).T
        return pos

    @staticmethod
    def fill_indices(world, positions, fill):
        for position in positions:
            world[tuple(position)] = fill


def play_random():
    stats = []
    for sim in range(1):
        env = SrYvlLvl0Env()
        env.render(mode="ansi")
        for i in range(50000):
            env.step(env.sample_action())
            env.render(mode="ansi")
            if env.done:
                break
        stats.append(env.stats_agg)
    pass


def human_play():
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt

    env = SrYvlLvl0Env()

    while not env.done:
        env.render(mode="human")
        img = env.observe()
        plt.imshow(np.moveaxis(img, 0, -1))
        plt.show()
        inp = input("qawdserc input: ")
        key = "qawdserc"
        if inp not in key:
            continue
        action = key.index(inp)
        x = env.step(action)
        print(env.legal_actions, env.agent_size)


def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6 * t**5 - 15 * t**4 + 10 * t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0 : res[0] : delta[0], 0 : res[1] : delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
    n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
    return np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)


def factors(n):
    return set(
        reduce(
            list.__add__,
            ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0),
        )
    )


def perlin():
    import matplotlib.pyplot as plt

    facs = sorted(list(factors(100)))
    print(facs)
    noise = generate_perlin_noise_2d(shape=(100, 100), res=[10, 10])
    plt.imshow((noise > 0) * 255, cmap="gray")
    plt.show()


if __name__ == "__main__":
    human_play()
