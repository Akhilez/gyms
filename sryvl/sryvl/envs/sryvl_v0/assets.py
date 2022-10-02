import numpy as np

PETAL_GOOD = [100, 200, 255]
PETAL_BAD = [255, 100, 100]
LEAF = [50, 150, 50]
STEM = [75, 50, 25]
SKIN = [255, 200, 0]
EYE = [0, 0, 0]
SHIRT = [255, 150, 200]
PANT = [25, 25, 75]
SHOES = [150, 150, 200]
PISTIL = [255, 200, 50]
TERRAIN = 75
BOUNDARY = 0

small_plant = [
    [2, 5, PETAL_GOOD],
    [3, 6, PETAL_GOOD],
    [3, 4, PETAL_GOOD],
    [4, 5, PETAL_GOOD],
    [3, 5, PISTIL],
    [4, 4, STEM],
    [4, 2, LEAF],
    [5, 3, STEM],
    [6, 4, LEAF],
    [6, 3, STEM],
    [7, 3, STEM],
]

medium_plant = [
    [2, 5, PETAL_GOOD],
    [3, 6, PETAL_GOOD],
    [3, 4, PETAL_GOOD],
    [4, 5, PETAL_GOOD],
    [3, 5, PISTIL],
    [4, 4, PETAL_GOOD],
    [4, 6, PETAL_GOOD],
    [2, 6, PETAL_GOOD],
    [2, 4, PETAL_GOOD],
    [4, 2, LEAF],
    [5, 3, STEM],
    [6, 4, LEAF],
    [6, 3, STEM],
    [7, 3, STEM],
]

large_plant = [
    [2, 5, PETAL_GOOD],
    [3, 6, PETAL_GOOD],
    [3, 4, PETAL_GOOD],
    [4, 5, PETAL_GOOD],
    [3, 5, PISTIL],
    [4, 4, PETAL_GOOD],
    [4, 6, PETAL_GOOD],
    [2, 6, PETAL_GOOD],
    [2, 4, PETAL_GOOD],
    [1, 5, PETAL_GOOD],
    [3, 7, PETAL_GOOD],
    [3, 3, PETAL_GOOD],
    [5, 5, PETAL_GOOD],
    [4, 2, LEAF],
    [5, 3, STEM],
    [6, 4, LEAF],
    [6, 3, STEM],
    [7, 3, STEM],
]

very_large_plant = [
    [1, 6, PETAL_GOOD],
    [1, 4, PETAL_GOOD],
    [2, 7, PETAL_GOOD],
    [2, 3, PETAL_GOOD],
    [4, 7, PETAL_GOOD],
    [4, 3, PETAL_GOOD],
    [5, 6, PETAL_GOOD],
    [5, 4, PETAL_GOOD],
    [2, 5, PETAL_GOOD],
    [3, 6, PETAL_GOOD],
    [3, 4, PETAL_GOOD],
    [4, 5, PETAL_GOOD],
    [3, 5, PISTIL],
    [4, 4, PETAL_GOOD],
    [4, 6, PETAL_GOOD],
    [2, 6, PETAL_GOOD],
    [2, 4, PETAL_GOOD],
    [1, 5, PETAL_GOOD],
    [3, 7, PETAL_GOOD],
    [3, 3, PETAL_GOOD],
    [5, 5, PETAL_GOOD],
    [4, 2, LEAF],
    [5, 3, STEM],
    [6, 4, LEAF],
    [6, 3, STEM],
    [7, 3, STEM],
]

plants = [small_plant, medium_plant, large_plant, very_large_plant]

small_poisonous_plant = [
    [2, 5, PETAL_BAD],
    [3, 6, PETAL_BAD],
    [3, 4, PETAL_BAD],
    [4, 5, PETAL_BAD],
    [3, 5, PISTIL],
    [4, 4, STEM],
    [4, 2, LEAF],
    [5, 3, STEM],
    [6, 4, LEAF],
    [6, 3, STEM],
    [7, 3, STEM],
]

medium_poisonous_plant = [
    [2, 5, PETAL_BAD],
    [3, 6, PETAL_BAD],
    [3, 4, PETAL_BAD],
    [4, 5, PETAL_BAD],
    [3, 5, PISTIL],
    [4, 4, PETAL_BAD],
    [4, 6, PETAL_BAD],
    [2, 6, PETAL_BAD],
    [2, 4, PETAL_BAD],
    [4, 2, LEAF],
    [5, 3, STEM],
    [6, 4, LEAF],
    [6, 3, STEM],
    [7, 3, STEM],
]

large_poisonous_plant = [
    [2, 5, PETAL_BAD],
    [3, 6, PETAL_BAD],
    [3, 4, PETAL_BAD],
    [4, 5, PETAL_BAD],
    [3, 5, PISTIL],
    [4, 4, PETAL_BAD],
    [4, 6, PETAL_BAD],
    [2, 6, PETAL_BAD],
    [2, 4, PETAL_BAD],
    [1, 5, PETAL_BAD],
    [3, 7, PETAL_BAD],
    [3, 3, PETAL_BAD],
    [5, 5, PETAL_BAD],
    [4, 2, LEAF],
    [5, 3, STEM],
    [6, 4, LEAF],
    [6, 3, STEM],
    [7, 3, STEM],
]

very_large_poisonous_plant = [
    [1, 6, PETAL_BAD],
    [1, 4, PETAL_BAD],
    [2, 7, PETAL_BAD],
    [2, 3, PETAL_BAD],
    [4, 7, PETAL_BAD],
    [4, 3, PETAL_BAD],
    [5, 6, PETAL_BAD],
    [5, 4, PETAL_BAD],
    [2, 5, PETAL_BAD],
    [3, 6, PETAL_BAD],
    [3, 4, PETAL_BAD],
    [4, 5, PETAL_BAD],
    [3, 5, PISTIL],
    [4, 4, PETAL_BAD],
    [4, 6, PETAL_BAD],
    [2, 6, PETAL_BAD],
    [2, 4, PETAL_BAD],
    [1, 5, PETAL_BAD],
    [3, 7, PETAL_BAD],
    [3, 3, PETAL_BAD],
    [5, 5, PETAL_BAD],
    [4, 2, LEAF],
    [5, 3, STEM],
    [6, 4, LEAF],
    [6, 3, STEM],
    [7, 3, STEM],
]

poisons = [small_poisonous_plant, medium_poisonous_plant, large_poisonous_plant, very_large_poisonous_plant]

agent = [
    [1, 6, SKIN],
    [1, 5, SKIN],
    [1, 4, SKIN],
    [1, 3, SKIN],
    [1, 2, SKIN],
    [2, 6, SKIN],
    [2, 5, EYE],
    [2, 4, SKIN],
    [2, 3, EYE],
    [2, 2, SKIN],
    [3, 6, SKIN],
    [3, 5, SKIN],
    [3, 4, SKIN],
    [3, 3, SKIN],
    [3, 2, SKIN],
    [4, 4, SKIN],
    [5, 6, SKIN],
    [5, 2, SKIN],
    [5, 5, SHIRT],
    [5, 4, SHIRT],
    [5, 3, SHIRT],
    [6, 4, PANT],
    [7, 5, SHOES],
    [7, 3, SHOES],
]

plant_in_hand = [
    [3, 7, PETAL_GOOD],
    [4, 8, PETAL_GOOD],
    [4, 6, PETAL_GOOD],
    [5, 7, PETAL_GOOD],
    [4, 7, PISTIL],
    [6, 6, STEM],
]

poison_in_hand = [
    [3, 1, PETAL_BAD],
    [4, 0, PETAL_BAD],
    [4, 2, PETAL_BAD],
    [5, 1, PETAL_BAD],
    [4, 1, PISTIL],
    [6, 2, STEM],
]


def build_cell(
        content,
        energy_level=1.0,
        reddish_threshold=0.2,
        jumper_threshold=1.5,
        distance_from_center=0.0,
        terrain_background=False,
        is_boundary=False,
):
    cell = np.ones((3, 9, 9), dtype=int)

    if is_boundary:
        return cell * BOUNDARY

    cell *= TERRAIN if terrain_background else 255

    if energy_level < reddish_threshold:
        skin_color = [255, 100, 100]
    elif energy_level > jumper_threshold:
        skin_color = [100, 255, 100]
    else:
        skin_color = SKIN

    for y, x, color in content:
        if color == SKIN:
            color = skin_color
        cell[:, y, x] = color

    cell -= int(distance_from_center * 20)
    cell = np.maximum(cell, 0)

    return cell


def make_obs(window, plant_inventory: int, poison_inventory: int, jumper_threshold: float):
    """
    planes:
    1: Boundary
    2: Terrain
    3: Food Ages
    4: Poison Ages
    5: Player Health
    6: Dist b/w center of the map to each point
    7: Previous path of the player health
    """
    img = np.zeros((3, 7*9, 7*9), dtype=np.uint8)
    for i in range(7):
        for j in range(7):
            (
                boundary,
                terrain,
                plant_age,
                poison_age,
                health,
                distance,
                _
            ) = window[:, i, j]

            content = []
            terrain_background = False
            energy_level = 1

            if boundary > 0:
                pass
            elif plant_age > 0:
                # Index of the size of the plant. (binning)
                plant_size_category = int(plant_age * len(plants))
                content = plants[plant_size_category]
            elif poison_age > 0:
                # Index of the size of the plant. (binning)
                plant_size_category = int(poison_age * len(poisons))
                content = poisons[plant_size_category]
            elif health > 0:
                energy_level = health
                content = agent
                if plant_inventory > 0:
                    content += plant_in_hand
                if poison_inventory > 0:
                    content += poison_in_hand
            if terrain > 0:
                content += []
                terrain_background = True

            cell = build_cell(
                content,
                energy_level=energy_level,
                reddish_threshold=0.2,
                jumper_threshold=jumper_threshold,
                distance_from_center=distance,
                terrain_background=terrain_background,
                is_boundary=boundary > 0,
            )
            img[:, i*9: (i+1) * 9, j*9: (j+1) * 9] = cell
    return img


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt

    # cell = np.ones_like(build_cell([])) * 75
    cell = build_cell(agent + plant_in_hand + poison_in_hand, energy_level=1, distance_from_center=0.9)

    cell = np.moveaxis(cell, 0, -1)
    plt.imshow(cell)
    plt.show()
