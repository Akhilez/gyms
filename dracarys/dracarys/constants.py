from gym.spaces import Discrete, Tuple, Box

# Collision Filter Categories
CAT_WALL = 1
CAT_ROCK = 2
CAT_TOWER = 7
CAT_DRAGON_WALK = 3
CAT_DRAGON_FLY = 4
CAT_ANIMAL = 5
CAT_ARROW = 6
CAT_GROUND = 7

# Sprite Lists
SPRITE_LIST_STATIC = 'Static'
SPRITE_LIST_DYNAMIC = 'Dynamic'

# Action Spaces
DRAGON_ACTION_SPACE = Tuple(
    (
        Box(-1, 1, shape=(3,)),  # Force direction x, y and rotation direction r
        Discrete(3),  # Action index (like fire, eat)
    ),
)


class DiscreteActions:
    NOOP = 0
    FIRE = 1
    ACT = 2
