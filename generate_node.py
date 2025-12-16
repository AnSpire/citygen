import random
from typing import List, Tuple
from config import CityConfig


config = CityConfig()


def random_steps(grid, base, spread):
    # base — средний размер квартала
    # spread — насколько кварталы могут отличаться
    steps = [base + random.uniform(-spread, spread) for _ in range(grid)]
    coords = [0]
    for s in steps:
        coords.append(coords[-1] + s)
    return coords


def generate_main_street_nodes(grid, base=300.0, spread=107) -> List[Tuple[float, float]]:
    """
    Генерирует главный ряд узлов (горизонтальная магистраль).
    grid — количество точек (например, 4)
    """

    xs = [0]
    # случайные шаги между точками по X
    for _ in range(grid - 1):
        step = base + random.uniform(-spread, spread)
        xs.append(xs[-1] + step)

    main_nodes = []

    for x in xs:
        # небольшой шум
        nx = x + random.uniform(-config.OFFSET, config.OFFSET)
        ny = random.uniform(-config.OFFSET, config.OFFSET)  # магистраль почти горизонтальная

        main_nodes.append((nx, ny))

    return main_nodes


def generate_block_nodes_from_road_down(top_side, rows, min_d=200, max_d=300) -> List[List[Tuple[float, float]]]:
    """
    main_row — список точек магистрали [(x,y), ..., (x,y)]
    rows — сколько рядов кварталов сгенерировать ниже магистрали
    """

    grid = len(top_side)
    nodes = [top_side]   # первый ряд уже задан

    for i in range(1, rows + 1):
        prev_row = nodes[i - 1]
        new_row = []

        for j in range(grid):

            # базовая точка — проекция вниз от prev_row[j]
            px, py = prev_row[j]

            # шаг вниз
            dy = random.uniform(min_d, max_d)
            y = py - dy  # кварталы идут "вниз"

            # небольшой шум
            x = px + random.uniform(-config.OFFSET, config.OFFSET)
            y = y + random.uniform(-config.OFFSET, config.OFFSET)

            # корректируем горизонтальное расстояние между соседями
            if j > 0:
                prev_x, prev_y = new_row[j - 1]
                dx = x - prev_x

                if dx < min_d:
                    x = prev_x + min_d
                if dx > max_d:
                    x = prev_x + max_d

            new_row.append((x, y))

        nodes.append(new_row)

    return nodes



def generate_block_nodes_from_road_up(bottom_side, rows, min_d=200, max_d=300) -> List[List[Tuple[float, float]]]:
    """
    main_row — список точек магистрали [(x,y), ..., (x,y)]
    rows — сколько рядов кварталов сгенерировать ниже магистрали
    """

    grid = len(bottom_side)
    nodes = [bottom_side]   # первый ряд уже задан

    for i in range(1, rows + 1):
        prev_row = nodes[i - 1]
        new_row = []

        for j in range(grid):

            # базовая точка — проекция вниз от prev_row[j]
            px, py = prev_row[j]

            # шаг вниз
            dy = random.uniform(min_d, max_d)
            y = py + dy  # кварталы идут "вниз"

            # небольшой шум
            x = px + random.uniform(-config.OFFSET, config.OFFSET)
            y = y + random.uniform(-config.OFFSET, config.OFFSET)

            # корректируем горизонтальное расстояние между соседями
            if j > 0:
                prev_x, prev_y = new_row[j - 1]
                dx = x - prev_x

                if dx < min_d:
                    x = prev_x + min_d
                if dx > max_d:
                    x = prev_x + max_d

            new_row.append((x, y))

        nodes.append(new_row)

    return nodes


def generate_block_nodes_from_road_right_down(
    top_side,
    left_side,
    rows,
    min_d=200,
    max_d=300
) -> List[List[Tuple[float, float]]]:
    """
    top_side  — верхняя граница (магистраль)
    left_side — левая граница
    rows      — сколько рядов генерировать вниз
    """

    grid = len(top_side)
    nodes = [top_side]   # первый ряд — верхняя сторона

    for i in range(1, rows + 1):
        prev_row = nodes[i - 1]
        new_row = []

        # базовая X-точка для текущего ряда — из левой стороны
        base_lx, base_ly = left_side[i]

        for j in range(grid):

            # --- базовая точка ---
            # X — от левой стороны (движение вправо)
            px = base_lx
            # Y — от предыдущего ряда (движение вниз)
            _, py = prev_row[j]

            # шаг вправо
            dx = random.uniform(min_d, max_d)
            x = px + dx

            # шаг вниз
            dy = random.uniform(min_d, max_d)
            y = py - dy

            # шум
            x += random.uniform(-config.OFFSET, config.OFFSET)
            y += random.uniform(-config.OFFSET, config.OFFSET)

            # --- корректировка по Y (между соседями в ряду) ---
            if j > 0:
                prev_x, prev_y = new_row[j - 1]
                dy_local = prev_y - y

                if dy_local < min_d:
                    y = prev_y - min_d
                if dy_local > max_d:
                    y = prev_y - max_d

            new_row.append((x, y))

        nodes.append(new_row)

    return nodes

