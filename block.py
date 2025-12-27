from typing import List

from shapely import LineString

from .config import CityConfig
from .houses import HouseGenerator
from .models import Block
from .generate_node import NodeGenerator
from .roads import RoadBuilder


class BlockBuilder:
    def __init__(self, config: CityConfig):
        self.config = config
        self.node_generator = NodeGenerator(config)
        self.road_builder = RoadBuilder()
        self.house_generator = HouseGenerator(config)

    def _finalize_block(self, nodes: List[List[tuple]]) -> Block:
        roads: List[LineString] = self.road_builder.generate_roads_from_grid(nodes)
        houses = [] if self.config.ANIMATE_HOUSES else self.house_generator.generate_houses(nodes, self.config.CELL, roads)
        return Block(nodes=nodes, roads=roads, houses=houses)

    def create_block_down(self, top_side: LineString) -> Block:
        block_nodes = self.node_generator.generate_block_nodes_from_road_down(top_side=list(top_side.coords), rows=2)
        return self._finalize_block(block_nodes)

    def create_block_up(self, bottom_side: LineString) -> Block:
        block_nodes = self.node_generator.generate_block_nodes_from_road_up(bottom_side=list(bottom_side.coords), rows=2)
        return self._finalize_block(block_nodes)

    def create_block_right_down(self, top_side: LineString, left_side: LineString) -> Block:
        block_nodes = self.node_generator.generate_block_nodes_from_road_right_down(top_side=list(top_side.coords), left_side=list(left_side.coords), rows=2)
        return self._finalize_block(block_nodes)

    def create_block_up_right(self, bottom_side: LineString, left_side: LineString) -> Block:
        block_nodes = self.node_generator.generate_block_nodes_from_road_up_right(
            bottom_side=list(bottom_side.coords),
            left_side=list(left_side.coords),
            rows=2,
        )
        return self._finalize_block(block_nodes)
    
    def create_block_between_roads(
        self,
        top_side: LineString,
        bottom_side: LineString,
    ) -> Block:
        block_nodes = self.node_generator.generate_block_nodes_between_top_bottom(
            top_side=list(top_side.coords),
            bottom_side=list(bottom_side.coords),
            rows=2,
        )
        return self._finalize_block(block_nodes)


