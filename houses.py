import math
import random
from typing import List

import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point, Polygon

from config import CityConfig
from models import Point2D


class HouseGenerator:
    def __init__(self, config: CityConfig):
        self.config = config

    def generate_houses(self, nodes: List[List[Point2D]], cell_size: float, roads, ax=None):
        houses: List[Polygon] = []

        rows = len(nodes) - 1
        cols = len(nodes[0]) - 1

        sq_size = cell_size * 0.11
        sq_spacing = cell_size * 0.02
        edge_len = cell_size * 0.27
        edge_height = cell_size * 0.12
        road_offset = cell_size * 0.14

        for i in range(rows):
            for j in range(cols):
                p_tl = nodes[i][j]
                p_tr = nodes[i][j + 1]
                p_br = nodes[i + 1][j + 1]
                p_bl = nodes[i + 1][j]
                cell = Polygon([p_tl, p_tr, p_br, p_bl])

                edges = [
                    LineString([p_tl, p_tr]),
                    LineString([p_tr, p_br]),
                    LineString([p_br, p_bl]),
                    LineString([p_bl, p_tl]),
                ]

                for edge in edges:
                    (x1, y1), (x2, y2) = edge.coords[:2]
                    dx, dy = x2 - x1, y2 - y1
                    length = math.hypot(dx, dy)
                    if length == 0:
                        continue

                    ux, uy = dx / length, dy / length
                    nx, ny = -uy, ux

                    step = 0.023 * length
                    house_len = edge_len
                    total = 0.3 * length

                    while total + house_len < length * 0.95:
                        bx = x1 + ux * total
                        by = y1 + uy * total

                        testx = bx + nx * road_offset
                        testy = by + ny * road_offset
                        if not Point(testx, testy).within(cell):
                            nx, ny = -nx, -ny

                        hx = bx + nx * road_offset
                        hy = by + ny * road_offset
                        house = Polygon(
                            [
                                (hx - ux * edge_len / 2 - nx * edge_height / 2, hy - uy * edge_len / 2 - ny * edge_height / 2),
                                (hx + ux * edge_len / 2 - nx * edge_height / 2, hy + uy * edge_len / 2 + -ny * edge_height / 2),
                                (hx + ux * edge_len / 2 + nx * edge_height / 2, hy + uy * edge_len / 2 + ny * edge_height / 2),
                                (hx - ux * edge_len / 2 + nx * edge_height / 2, hy - uy * edge_len / 2 + ny * edge_height / 2),
                            ]
                        )

                        houses.append(house)
                        if self.config.SHOW_LOCAL and self.config.ANIMATE_HOUSES:
                            x, y = house.exterior.xy
                            ax.fill(x, y, color="brown", alpha=1, edgecolor="black", linewidth=1)
                            ax.figure.canvas.draw_idle()
                            plt.pause(0.001)
                        total += house_len + step

                num_sq = random.randint(5, 9)
                min_x = min(p_tl[0], p_tr[0], p_bl[0], p_br[0])
                max_x = max(p_tl[0], p_tr[0], p_bl[0], p_br[0])
                min_y = min(p_tl[1], p_tr[1], p_bl[1], p_br[1])
                max_y = max(p_tl[1], p_tr[1], p_bl[1], p_br[1])

                for _ in range(num_sq):
                    for _attempt in range(15):
                        hx = random.uniform(min_x + sq_spacing, max_x - sq_size - sq_spacing)
                        hy = random.uniform(min_y + sq_spacing, max_y - sq_size - sq_spacing)
                        house = Polygon([(hx, hy), (hx + sq_size, hy), (hx + sq_size, hy + sq_size), (hx, hy + sq_size)])

                        if house.within(cell) and all(house.distance(h) > sq_spacing for h in houses):
                            houses.append(house)
                            if self.config.SHOW_LOCAL and self.config.ANIMATE_HOUSES:
                                x, y = house.exterior.xy
                                ax.fill(x, y, color="brown", alpha=1, edgecolor="black", linewidth=1)
                                ax.figure.canvas.draw_idle()
                                plt.pause(0.001)
                            break
        return houses
