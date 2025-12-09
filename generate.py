import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.affinity import translate
import matplotlib.pyplot as plt
import math
import random
from generate_node import  *
from city_border import get_city_border
from roads import generate_roads
from branches import generate_branches
from houses import generate_houses
from config import CityConfig
"""
РАЗНЫЙ РАЗМЕР КВАРТАЛОВ
"""
config = CityConfig()

main_street = generate_main_street(6)
block = generate_blocks_from_main(main_row=main_street[1:-1], rows=2)
nodes = block.copy()
nodes.append(main_street)
roads = generate_roads(block)
all_roads = roads
CITY_BORDER = get_city_border(block)


# === ЭТАП 1 — рисуем и показываем только дороги ===
if config.SHOW_LOCAL:
    plt.ion()
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect("equal")
    ax.set_xlim(-2000, 2000)
    ax.set_ylim(-2000, 2000)
    for row in nodes:
        for x, y in row:
            ax.scatter(x, y, color="red", s=10)
    plt.show()
    plt.pause(5)         # обновление окна

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

