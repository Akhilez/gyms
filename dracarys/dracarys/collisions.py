from pymunk import Arbiter
from dracarys.constants import CAT_ARROW, CAT_DRAGON_WALK, CAT_DRAGON_FLY


def collision_post(arbiter: Arbiter, space, data):
    a, b = arbiter.shapes
    for shape, other in ((a, b), (b, a)):
        if shape.filter.categories in (CAT_ARROW, CAT_DRAGON_WALK, CAT_DRAGON_FLY):
            shape.parent.on_collision(other)
