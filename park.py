from __future__ import annotations

import random
from typing import List

import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, LineString


# ==============================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==============================

def random_point_in_polygon(poly: Polygon) -> Point:
    min_x, min_y, max_x, max_y = poly.bounds
    while True:
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        p = Point(x, y)
        if poly.contains(p):
            return p


# ==============================
# ГЕНЕРАЦИЯ ПАРКА
# ==============================

import numpy as np
from shapely.geometry import Polygon

def generate_park_polygon() -> Polygon:
    m = 50

    # === ПЕРВЫЕ ДВЕ СТОРОНЫ — КАК И РАНЬШЕ ===
    P0 = np.array([0.0 * m, 0.0 * m])   # (0, 0)
    P1 = np.array([8.0 * m, 1.0 * m])   # (8, 1)
    P2 = np.array([10.0 * m, 4.0 * m])  # (10, 4)

    # Вектора первых двух сторон
    v1 = P1 - P0            # сторона P0 → P1
    v2 = P2 - P1            # сторона P1 → P2

    # Остальные вершины задаём относительно v1 и v2 так,
    # чтобы форма совпала с исходной:
    #
    # P3 = (9, 8)
    # P4 = (5,10)
    # P5 = (1, 9)
    # P6 = (-1,5)
    # P7 = (-2,2)
    #
    # Pi = P0 + a_i * v1 + b_i * v2

    rel_coeffs = [
        (1/2, 5/2),          # даёт (9, 8)
        (-5/22, 75/22),      # даёт (5, 10)
        (-15/22, 71/22),     # даёт (1, 9)
        (-13/22, 41/22),     # даёт (-1, 5)
        (-5/11, 9/11),       # даёт (-2, 2)
    ]

    points = [tuple(P0), tuple(P1), tuple(P2)]

    for a, b in rel_coeffs:
        pt = P0 + a * v1 + b * v2
        points.append(tuple(pt))

    return Polygon(points)



def generate_trees(park: Polygon, n_trees: int = 80) -> List[Point]:
    return [random_point_in_polygon(park) for _ in range(n_trees)]


def generate_lawns(park: Polygon, n_lawns: int = 3) -> List[Polygon]:
    lawns: List[Polygon] = []
    for _ in range(n_lawns):
        center = random_point_in_polygon(park)
        w = random.uniform(0.8, 1.5)
        h = random.uniform(0.6, 1.2)
        cx, cy = center.x, center.y

        rect = Polygon([
            (cx - w / 2, cy - h / 2),
            (cx + w / 2, cy - h / 2),
            (cx + w / 2, cy + h / 2),
            (cx - w / 2, cy + h / 2),
        ])

        if park.contains(rect):
            lawns.append(rect)
        else:
            clipped = rect.intersection(park)
            if clipped and not clipped.is_empty:
                if isinstance(clipped, Polygon):
                    lawns.append(clipped)
                else:
                    for geom in clipped.geoms:
                        if isinstance(geom, Polygon):
                            lawns.append(geom)
    return lawns


def generate_paths(park: Polygon, n_paths: int = 4) -> List[LineString]:
    paths: List[LineString] = []
    for _ in range(n_paths):
        k = random.randint(3, 5)
        pts = [random_point_in_polygon(park) for _ in range(k)]
        line = LineString([(p.x, p.y) for p in pts])
        clipped = line.intersection(park)
        if clipped.is_empty:
            continue
        if isinstance(clipped, LineString):
            paths.append(clipped)
        else:
            for geom in clipped.geoms:
                if isinstance(geom, LineString):
                    paths.append(geom)
    return paths


# ==============================
# ОТДЕЛЬНЫЕ ФУНКЦИИ ОТРИСОВКИ
# ==============================

def draw_polygon(ax: plt.Axes, poly: Polygon) -> None:
    """
    Отрисовать многоугольник: точки, рёбра, заливка.
    """
    # точки
    coords = list(poly.exterior.coords)[:-1]
    vx = [p[0] for p in coords]
    vy = [p[1] for p in coords]
    ax.scatter(vx, vy, color="red", s=10, zorder=3)

    # рёбра
    x, y = poly.exterior.xy
    ax.plot(x, y, color="black", linewidth=2, zorder=2)

    # заливка
    ax.fill(x, y, color="#c8f7c5", alpha=0.7, zorder=1)


def draw_lawns(ax: plt.Axes, lawns: List[Polygon]) -> None:
    """
    Отрисовать все лужайки.
    """
    for lawn in lawns:
        if lawn.is_empty:
            continue
        x, y = lawn.exterior.xy
        ax.fill(x, y, color="#a8e6a3", alpha=0.9, zorder=1.5)


def draw_paths(ax: plt.Axes, paths: List[LineString]) -> None:
    """
    Отрисовать тропинки.
    """
    for path in paths:
        if path.is_empty:
            continue
        x, y = path.xy
        ax.plot(x, y, color="gray", linewidth=2, linestyle="--", zorder=2.5)


def draw_trees(ax: plt.Axes, trees: List[Point]) -> None:
    """
    Отрисовать деревья.
    """
    tx = [t.x for t in trees]
    ty = [t.y for t in trees]
    ax.scatter(tx, ty, color="green", s=15, zorder=3)


# ==============================
# ГЛАВНАЯ ФУНКЦИЯ
# ==============================

def plot_park() -> None:
    park = generate_park_polygon()
    trees = generate_trees(park, n_trees=80)
    lawns = generate_lawns(park, n_lawns=4)
    paths = generate_paths(park, n_paths=4)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal", "box")

    draw_polygon(ax, park)
    draw_lawns(ax, lawns)
    draw_paths(ax, paths)
    draw_trees(ax, trees)

    # Отступы от границ парка
    min_x, min_y, max_x, max_y = park.bounds
    margin = 1.0
    ax.set_xlim(min_x - margin, max_x + margin)
    ax.set_ylim(min_y - margin, max_y + margin)

    ax.set_title("Сгенерированный парк (shapely + matplotlib)")
    ax.grid(True, alpha=0.2)

    plt.show()


if __name__ == "__main__":
    random.seed(42)
    plot_park()
