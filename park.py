from __future__ import annotations

import random
from typing import List

import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, LineString


# ==============================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==============================

def random_point_in_polygon(poly: Polygon) -> Point:
    """
    Возвращает случайную точку внутри многоугольника poly.
    Используется простая rejection-sampling по bounding box многоугольника.
    """
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

def generate_park_polygon() -> Polygon:
    """
    Задаём произвольный многоугольник парка.
    Если нужно — можно заменить координаты на свои.
    """
    coords = [
        (0.0, 0.0),
        (8.0, 1.0),
        (10.0, 4.0),
        (9.0, 8.0),
        (5.0, 10.0),
        (1.0, 9.0),
        (-1.0, 5.0),
        (-2.0, 2.0),
    ]
    return Polygon(coords)


def generate_trees(park: Polygon, n_trees: int = 80) -> List[Point]:
    """
    Генерируем деревья как точки внутри парка.
    """
    trees: List[Point] = []
    for _ in range(n_trees):
        trees.append(random_point_in_polygon(park))
    return trees


def generate_lawns(park: Polygon, n_lawns: int = 3) -> List[Polygon]:
    """
    Генерируем лужайки как маленькие прямоугольные многоугольники
    внутри парка.
    """
    lawns: List[Polygon] = []
    min_x, min_y, max_x, max_y = park.bounds

    for _ in range(n_lawns):
        # центр лужайки — случайная точка внутри парка
        center: Point = random_point_in_polygon(park)

        # случайный размер
        w = random.uniform(0.8, 1.5)
        h = random.uniform(0.6, 1.2)

        cx, cy = center.x, center.y
        rect = Polygon([
            (cx - w / 2, cy - h / 2),
            (cx + w / 2, cy - h / 2),
            (cx + w / 2, cy + h / 2),
            (cx - w / 2, cy + h / 2),
        ])

        # Можно отфильтровать, чтобы лужайка целиком была внутри парка
        if park.contains(rect):
            lawns.append(rect)
        else:
            # если чуть вылезла — можно просто пересечь с парком
            rect_clipped = rect.intersection(park)
            if not rect_clipped.is_empty:
                lawns.append(rect_clipped)

    return lawns


def generate_paths(park: Polygon, n_paths: int = 4) -> List[LineString]:
    """
    Генерируем тропинки как ломаные линии (LineString) внутри парка.
    Каждая тропинка — 3–5 сегментов.
    """
    paths: List[LineString] = []

    for _ in range(n_paths):
        k = random.randint(3, 5)  # количество узлов тропинки
        points: List[Point] = [random_point_in_polygon(park) for _ in range(k)]

        coords = [(p.x, p.y) for p in points]
        line = LineString(coords)

        # Можно дополнительно ограничить, чтобы тропинка была внутри парка
        line_clipped = line.intersection(park)
        if not line_clipped.is_empty:
            # intersection может вернуть как LineString, так и MultiLineString,
            # но для простоты возьмём только LineString-и.
            if isinstance(line_clipped, LineString):
                paths.append(line_clipped)
            else:
                for geom in line_clipped.geoms:
                    if isinstance(geom, LineString):
                        paths.append(geom)

    return paths


# ==============================
# ОТРИСОВКА
# ==============================

def plot_park() -> None:
    # --- генерация объектов shapely ---
    park: Polygon = generate_park_polygon()
    trees: List[Point] = generate_trees(park, n_trees=80)
    lawns: List[Polygon] = generate_lawns(park, n_lawns=4)
    paths: List[LineString] = generate_paths(park, n_paths=4)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal", "box")

    # === 1) Вершины парка как красные точки ===
    # Берём координаты внешнего контура (без последней дублирующей точки)
    exterior_coords = list(park.exterior.coords)[:-1]
    vx = [c[0] for c in exterior_coords]
    vy = [c[1] for c in exterior_coords]
    ax.scatter(vx, vy, color="red", s=40, zorder=3, label="Вершины парка")

    # === 2) Рёбра парка — чёрные линии ===
    px, py = park.exterior.xy
    ax.plot(px, py, color="black", linewidth=2, zorder=2, label="Граница парка")

    # === 3) Заливка многоугольника парка ===
    ax.fill(px, py, color="#c8f7c5", alpha=0.7, zorder=1, label="Парк")

    # === 4) Лужайки (Polygon из shapely) ===
    for lawn in lawns:
        if lawn.is_empty:
            continue
        lx, ly = lawn.exterior.xy
        ax.fill(lx, ly, color="#a8e6a3", alpha=0.9, zorder=1.5)

    # === 5) Тропинки — LineString ===
    for path in paths:
        if path.is_empty:
            continue
        x, y = path.xy
        ax.plot(x, y, color="gray", linewidth=2, linestyle="--", zorder=2.5)

    # === 6) Деревья — Point ===
    tx = [t.x for t in trees]
    ty = [t.y for t in trees]
    ax.scatter(tx, ty, color="green", s=15, zorder=3, label="Деревья")

    # Отступы от края
    min_x, min_y, max_x, max_y = park.bounds
    margin = 1.0
    ax.set_xlim(min_x - margin, max_x + margin)
    ax.set_ylim(min_y - margin, max_y + margin)

    ax.set_title("Сгенерированный парк (shapely + matplotlib)")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.2)

    plt.show()


if __name__ == "__main__":
    # Для повторяемости можно зафиксировать seed
    random.seed(42)
    plot_park()
