import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.affinity import translate
import matplotlib.pyplot as plt
import math
import random
from generate_node import  *
from city_border import get_city_border
from roads import generate_roads_from_grid, generate_road_from_points
from branches import generate_branches
from houses import generate_houses
from config import CityConfig
"""
РАЗНЫЙ РАЗМЕР КВАРТАЛОВ
"""
config = CityConfig()

main_street_nodes = generate_main_street(8)
block = generate_blocks_from_main_down(main_row=main_street_nodes[2:-2], rows=2)
# block2 = generate_blocks_from_main(main_row=block[-1], rows = 2)
# block += block2
nodes = block.copy()
nodes.append(main_street_nodes)
roads: List[LineString] = generate_roads_from_grid(block)
main_street_road: List[LineString] = generate_road_from_points(main_street_nodes)
all_roads = roads + main_street_road
CITY_BORDER = get_city_border(block)


# === ЭТАП 1 — рисуем и показываем только дороги ===
if config.SHOW_LOCAL:
    plt.ion()
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect("equal")
    ax.set_xlim(-3000, 3000)
    ax.set_ylim(-3000, 3000)
    for row in nodes:
        for x, y in row:
            ax.scatter(x, y, color="red", s=10)
    plt.show()

    for r in all_roads:
        x, y = r.xy
        ax.plot(x, y, color="black", linewidth=1)


    houses = generate_houses(block, config.CELL, all_roads, ax)

    plt.show()
    plt.pause(0.1)

    # === ЭТАП 2 — дорисовываем дома ===

    # for house in houses:
    #     x, y = house.exterior.xy
    #     ax.fill(x, y, color="brown", alpha=1, edgecolor="black", linewidth=1)

    # узлы поверх

    plt.draw()
    plt.pause(1000)         # обновление окна

