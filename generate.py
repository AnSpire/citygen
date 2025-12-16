import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.affinity import translate
import matplotlib.pyplot as plt
from generate_node import  *
from city_border import get_city_border
from roads import generate_roads_from_grid, generate_road_from_points
from branches import generate_branches
from houses import generate_houses
from config import CityConfig
from park import *
from block import create_block_down, create_block_right_down
"""
РАЗНЫЙ РАЗМЕР КВАРТАЛОВ
"""
config = CityConfig()


main_street_nodes: List[Tuple[float, float]] = generate_main_street_nodes(10)
main_street_road: List[LineString] = generate_road_from_points(main_street_nodes)

first_block = create_block_down(top_side=LineString(main_street_nodes[5:-1]))
nodes = list(first_block["nodes"])
nodes.append(main_street_nodes)
park_right_side: List[Tuple[float, float]] = [line[0] for line in first_block["nodes"]]

park_polygon = generate_park_polygon_from(LineString(park_right_side), LineString(main_street_nodes[3:5]))

bottom_park_side = reversed(park_polygon.exterior.coords[-5:-1])

second_block = create_block_down(top_side=LineString(bottom_park_side))

# second_block_left_side = [line[0] for line in second_block["nodes"]]
# print(second_block_left_side)
# park_right_side = 

# print("left_side", LineString(line[-1] for line in second_block["nodes"]))
# print("top_side", LineString(first_block["nodes"][-1]))
# input()
third_block = create_block_right_down(left_side=LineString(line[-1] for line in second_block["nodes"]), top_side=LineString(first_block["nodes"][-1]))

# print(first_block["roads"])
# print(main_street_road)
# input()

# blocks = [first_block, second_block, third_block]
blocks = [first_block, second_block, third_block]
all_roads = [
    road
    for block in blocks
    for road in block["roads"]
]

all_roads += main_street_road


if config.SHOW_LOCAL:
    plt.ion()
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect("equal")
    m = 3000
    ax.set_xlim(-m, m)
    ax.set_ylim(-m, m)
    for node in main_street_nodes:
        x, y = node
        ax.scatter(x, y, color="red", s=10)


    for block in blocks:
        for row in block["nodes"]:
            for x, y in row:
                ax.scatter(x, y, color="red", s=10)
        plt.show() 
        if config.ANIMATE_HOUSES:
            houses = generate_houses(block, config.CELL, all_roads, ax)
        else:
            for house in block["houses"]:
                x, y = house.exterior.xy
                ax.fill(x, y, color="brown", alpha=1, edgecolor="black", linewidth=1)
        plt.show()
        plt.pause(0.1)
    for r in all_roads:
        x, y = r.xy
        ax.plot(x, y, color="black", linewidth=1)
    
    draw_polygon(ax=ax, poly=park_polygon)
    plt.draw()
    plt.pause(1000)         # обновление окна

