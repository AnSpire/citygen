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

def create_block(main_street_nodes_part) -> dict:
    block = generate_block_nodes_from_main_down(main_row=main_street_nodes_part, rows=2)
    nodes = block.copy() 
    nodes.append(main_street_nodes)
    roads: List[LineString] = generate_roads_from_grid(block)
    # CITY_BORDER = get_city_border(block)
    if not config.ANIMATE_HOUSES:
        houses = generate_houses(block, config.CELL, roads)
    return {"nodes": nodes, "roads": roads, "houses": houses}

main_street_nodes: List[Tuple[float, float]] = generate_main_street_nodes(10)
main_street_road: List[LineString] = generate_road_from_points(main_street_nodes)

first_block = create_block(main_street_nodes_part=main_street_nodes[5:-1])

blocks = [first_block]

all_roads = first_block["roads"] + main_street_road


if config.SHOW_LOCAL:
    plt.ion()
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect("equal")
    ax.set_xlim(-3000, 3000)
    ax.set_ylim(-3000, 3000)
    for block in blocks:
        for row in block["nodes"]:
            for x, y in row:
                ax.scatter(x, y, color="red", s=10)
        plt.show()

        for r in all_roads:
            x, y = r.xy
            ax.plot(x, y, color="black", linewidth=1)

        if config.ANIMATE_HOUSES:
            houses = generate_houses(block, config.CELL, all_roads, ax)
        else:
            for house in block["houses"]:
                x, y = house.exterior.xy
                ax.fill(x, y, color="brown", alpha=1, edgecolor="black", linewidth=1)
        plt.show()
        plt.pause(0.1)

    plt.draw()
    plt.pause(1000)         # обновление окна

