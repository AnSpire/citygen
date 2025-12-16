import random
from typing import List, Tuple

import numpy as np
from shapely import LineString

Point2D = Tuple[float, float]


class RoadBuilder:
    def slightly_noisy_curve(self, p1: Point2D, p2: Point2D, rate: int) -> LineString:
        x1, y1 = p1
        x2, y2 = p2

        mid = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
        angle = random.uniform(0, 2 * np.pi)
        dist = random.uniform(1, 4)
        offset = np.array([np.cos(angle) * dist, np.sin(angle) * dist])

        mid = mid + offset + rate
        curve = LineString([p1, tuple(mid), p2])
        return curve.simplify(0.5)

    def generate_road_from_points(self, points: List[Point2D]) -> List[LineString]:
        """
        Строит одну дорогу по списку точек (p0→p1→p2→...).
        Работает только с одномерным массивом точек.
        """
        roads: List[LineString] = []
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            roads.append(LineString([p1, p2]))
        return roads

    def generate_roads_from_grid(self, nodes: List[List[Point2D]]) -> List[LineString]:
        """
        Строит дороги внутри района по двумерной сетке узлов.
        Горизонтальные + вертикальные соединения.
        """
        roads: List[LineString] = []
        rows = len(nodes)
        if rows == 0:
            return roads

        cols = len(nodes[0])
        for i in range(rows):
            for j in range(cols):
                if j + 1 < cols:
                    p1, p2 = nodes[i][j], nodes[i][j + 1]
                    roads.append(LineString([p1, p2]))
                if i + 1 < rows:
                    p1, p2 = nodes[i][j], nodes[i + 1][j]
                    roads.append(LineString([p1, p2]))
        return roads
