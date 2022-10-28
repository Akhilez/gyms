import math


def get_angle(a, b, c):
    return math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])


def get_distance(a, b):
    (x1, y1), (x2, y2) = a, b
    return math.hypot(x1 - x2, y1 - y2)
