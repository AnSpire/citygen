from typing import List, Tuple

import matplotlib.pyplot as plt
from shapely.geometry import LineString

from .block import BlockBuilder
from .branches import generate_branches
from .config import CityConfig
from .houses import HouseGenerator
from .models import CityLayout
from .park import ParkGenerator, draw_polygon
from  .roads import RoadBuilder


class CityGenerator:
    """
    Собирает все части генерации в единый пайплайн: магистраль, кварталы, парк.
    """

    def __init__(self, config: CityConfig):
        self.config = config
        self.block_builder = BlockBuilder(config)
        self.road_builder = RoadBuilder()
        self.house_generator = HouseGenerator(config)
        self.park_generator = ParkGenerator()

    def generate(self) -> CityLayout:
        main_street_nodes: List[Tuple[float, float]] = self.block_builder.node_generator.generate_main_street_nodes(10)
        main_street_roads: List[LineString] = self.road_builder.generate_road_from_points(main_street_nodes)

        first_block = self.block_builder.create_block_down(top_side=LineString(main_street_nodes[5:-1]))
        park_right_side: List[Tuple[float, float]] = [line[0] for line in first_block.nodes]

        park_polygon = self.park_generator.generate_polygon_from_sides(LineString(park_right_side), LineString(main_street_nodes[3:5]))
        bottom_park_side = list(reversed(park_polygon.exterior.coords[-5:-1]))

        second_block = self.block_builder.create_block_down(top_side=LineString(bottom_park_side))
        third_block = self.block_builder.create_block_right_down(left_side=LineString(line[-1] for line in second_block.nodes), top_side=LineString(first_block.nodes[-1]))

        fourth_block = self.block_builder.create_block_up(bottom_side=LineString(main_street_nodes[3:6]))

        fifth_block = self.block_builder.create_block_up_right(bottom_side=LineString(main_street_nodes[5:9]), left_side=LineString(line[-1] for line in fourth_block.nodes))

        new_main_street_nodes = self.block_builder.node_generator.generate_main_street_nodes_from(10, (0, -1550))
        new_main_street_roads = self.road_builder.generate_road_from_points(new_main_street_nodes)

        fourth_block = self.block_builder.create_block_between_roads(LineString(second_block.nodes[-1]), LineString(new_main_street_nodes[3:7]))
        blocks = [first_block, second_block, third_block, fourth_block, fifth_block]
        all_roads = [road for block in blocks for road in block.roads]
        all_roads += main_street_roads
        all_roads += new_main_street_roads

        return CityLayout(
            main_street_nodes=main_street_nodes + new_main_street_nodes,
            main_street_roads=main_street_roads,
            blocks=blocks,
            park_polygon=park_polygon,
            all_roads=all_roads,
        )


class CityPlotter:
    """
    Отвечает только за отрисовку результата.
    """

    def __init__(self, config: CityConfig, house_generator: HouseGenerator):
        self.config = config
        self.house_generator = house_generator

    def plot(self, layout: CityLayout):
        if not self.config.SHOW_LOCAL:
            return

        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect("equal")
        m = 3000
        ax.set_xlim(-m, m)
        ax.set_ylim(-m, m)

        for node in layout.main_street_nodes:
            x, y = node
            ax.scatter(x, y, color="red", s=10)


        for block in layout.blocks:
            for row in block.nodes:
                for x, y in row:
                    ax.scatter(x, y, color="red", s=10)

            if self.config.ANIMATE_HOUSES:
                self.house_generator.generate_houses(block.nodes, self.config.CELL, layout.all_roads, ax)
            else:
                for house in block.houses:
                    x, y = house.exterior.xy
                    ax.fill(x, y, color="brown", alpha=1, edgecolor="black", linewidth=1)
            plt.show()
            plt.pause(0.1)

        for road in layout.all_roads:
            x, y = road.xy
            ax.plot(x, y, color="black", linewidth=1)

        draw_polygon(ax=ax, poly=layout.park_polygon)
        plt.draw()
        plt.pause(1000)


def main():
    config = CityConfig()
    city_generator = CityGenerator(config)
    layout = city_generator.generate()


    plotter = CityPlotter(config, HouseGenerator(config))
    plotter.plot(layout)


if __name__ == "__main__":
    main()
