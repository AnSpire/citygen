from generate_node import generate_block_nodes_from_road_down, generate_block_nodes_from_road_right_down
from roads import generate_roads_from_grid
from houses import generate_houses
from config import CityConfig
from typing import List
from shapely import LineString


config = CityConfig()


def create_block_down(top_side: LineString) -> dict:
    block = generate_block_nodes_from_road_down(top_side=list(top_side.coords), rows=2)
    nodes = block.copy() 
    roads: List[LineString] = generate_roads_from_grid(block)
    # CITY_BORDER = get_city_border(block)
    if not config.ANIMATE_HOUSES:
        houses = generate_houses(block, config.CELL, roads)
    return {"nodes": nodes, "roads": roads, "houses": houses}



def create_block_up(bottom_side: LineString) -> dict:
    block = generate_block_nodes_from_road_down(top_side=list(bottom_side.coords), rows=2)
    nodes = block.copy() 
    roads: List[LineString] = generate_roads_from_grid(block)
    # CITY_BORDER = get_city_border(block)
    if not config.ANIMATE_HOUSES:
        houses = generate_houses(block, config.CELL, roads)
    return {"nodes": nodes, "roads": roads, "houses": houses}



def create_block_right_down(top_side: LineString, left_side: LineString) -> dict:
    block = generate_block_nodes_from_road_right_down(top_side=list(top_side.coords), left_side=list(left_side.coords), rows=2)
    nodes = block.copy() 
    roads: List[LineString] = generate_roads_from_grid(block)
    # CITY_BORDER = get_city_border(block)
    if not config.ANIMATE_HOUSES:
        houses = generate_houses(block, config.CELL, roads)
    return {"nodes": nodes, "roads": roads, "houses": houses}