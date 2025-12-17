import random
from typing import List, Tuple

from .config import CityConfig


class NodeGenerator:
    def __init__(self, config: CityConfig):
        self.config = config

    def generate_main_street_nodes(self, grid: int, base: float = 300.0, spread: float = 107.0) -> List[Tuple[float, float]]:
        """
        Генерирует главный ряд узлов (горизонтальная магистраль).
        grid — количество точек (например, 4)
        """
        xs = [0]
        for _ in range(grid - 1):
            step = base + random.uniform(-spread, spread)
            xs.append(xs[-1] + step)

        main_nodes = []
        for x in xs:
            nx = x + random.uniform(-self.config.OFFSET, self.config.OFFSET)
            ny = random.uniform(-self.config.OFFSET, self.config.OFFSET)
            main_nodes.append((nx, ny))
        return main_nodes

    def generate_block_nodes_from_road_down(self, top_side: List[Tuple[float, float]], rows: int, min_d: float = 200, max_d: float = 300) -> List[List[Tuple[float, float]]]:
        """
        main_row — список точек магистрали [(x,y), ..., (x,y)]
        rows — сколько рядов кварталов сгенерировать ниже магистрали
        """
        grid = len(top_side)
        nodes = [top_side]

        for i in range(1, rows + 1):
            prev_row = nodes[i - 1]
            new_row = []

            for j in range(grid):
                px, py = prev_row[j]
                dy = random.uniform(min_d, max_d)
                y = py - dy
                x = px + random.uniform(-self.config.OFFSET, self.config.OFFSET)
                y = y + random.uniform(-self.config.OFFSET, self.config.OFFSET)

                if j > 0:
                    prev_x, _prev_y = new_row[j - 1]
                    dx = x - prev_x
                    if dx < min_d:
                        x = prev_x + min_d
                    if dx > max_d:
                        x = prev_x + max_d
                new_row.append((x, y))
            nodes.append(new_row)
        return nodes

    def generate_block_nodes_from_road_up(self, bottom_side: List[Tuple[float, float]], rows: int, min_d: float = 200, max_d: float = 300) -> List[List[Tuple[float, float]]]:
        """
        main_row — список точек магистрали [(x,y), ..., (x,y)]
        rows — сколько рядов кварталов сгенерировать ниже магистрали
        """
        grid = len(bottom_side)
        nodes = [bottom_side]

        for i in range(1, rows + 1):
            prev_row = nodes[i - 1]
            new_row = []

            for j in range(grid):
                px, py = prev_row[j]
                dy = random.uniform(min_d, max_d)
                y = py + dy
                x = px + random.uniform(-self.config.OFFSET, self.config.OFFSET)
                y = y + random.uniform(-self.config.OFFSET, self.config.OFFSET)

                if j > 0:
                    prev_x, _prev_y = new_row[j - 1]
                    dx = x - prev_x
                    if dx < min_d:
                        x = prev_x + min_d
                    if dx > max_d:
                        x = prev_x + max_d
                new_row.append((x, y))
            nodes.append(new_row)
        return nodes

    def generate_block_nodes_from_road_right_down(
        self,
        top_side: List[Tuple[float, float]],
        left_side: List[Tuple[float, float]],
        rows: int,
        min_d: float = 200,
        max_d: float = 300,
    ) -> List[List[Tuple[float, float]]]:
        """
        top_side  — верхняя граница (магистраль)
        left_side — левая граница
        rows      — сколько рядов генерировать вниз
        """
        nodes = [top_side]
        for i in range(1, rows + 1):
            left_point = left_side[i]
            new_row: List[Tuple[float, float]] = [left_point]
            for _ in range(1, len(top_side)):
                x_prev, y_prev = new_row[-1]
                new_point = (
                    x_prev + random.uniform(min_d, max_d),
                    y_prev + random.uniform(-self.config.OFFSET, self.config.OFFSET),
                )
                new_row.append(new_point)
            nodes.append(new_row)
        return nodes
