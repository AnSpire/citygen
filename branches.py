import math
import random

from shapely import LineString

from .config import CityConfig
from .roads import RoadBuilder


config = CityConfig()
road_builder = RoadBuilder()


def generate_branches(roads, city_polygon):
    branches = []

    for road in roads:
        if not isinstance(road, LineString):
            continue

        mid = road.interpolate(0.4, normalized=True)
        x, y = mid.x, mid.y

        if random.random() > config.BRANCH_PROB:
            continue

        dx = road.coords[1][0] - road.coords[0][0]
        dy = road.coords[1][1] - road.coords[0][1]
        nx, ny = -dy, dx
        length = math.sqrt(nx * nx + ny * ny)
        nx, ny = nx / length, ny / length

        length_multiplier = config.CELL * random.uniform(config.BRANCH_MIN, config.BRANCH_MAX)
        if random.random() < 0.5:
            length_multiplier = -length_multiplier

        p2 = (x + nx * length_multiplier, y + ny * length_multiplier)
        branch = LineString(road_builder.slightly_noisy_curve((x, y), p2, rate=random.randint(0, 6)))

        if not city_polygon.contains(branch):
            continue

        branches.append(branch)

    return branches
