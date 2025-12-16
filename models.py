from dataclasses import dataclass
from typing import List, Tuple

from shapely.geometry import LineString, Polygon

Point2D = Tuple[float, float]


@dataclass
class Block:
    nodes: List[List[Point2D]]
    roads: List[LineString]
    houses: List[Polygon]


@dataclass
class CityLayout:
    main_street_nodes: List[Point2D]
    main_street_roads: List[LineString]
    blocks: List[Block]
    park_polygon: Polygon
    all_roads: List[LineString]
