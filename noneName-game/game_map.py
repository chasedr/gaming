import numpy as np  # type: ignore
from tcod.console import Console

import tile_types
import sqlite3


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.console = None
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")
        self.elevate = 25
        self.location = {'x': -832, 'z': 236}  # 位置坐标
        # self.tiles[30:70, 22] = tile_types.wall

        self.map = self.load_map_from_database("./maps/blocks.db", "blocks", self.location['x'], self.elevate, self.location['z'])  # 从数据库加载地图数据

        x_min = min(row[0] for row in self.map)
        z_min = min(row[2] for row in self.map)
        print(x_min, z_min)  # 打印最小值

        
        for row in self.map:
            x, y, z, name, p1, p2 = row
            tile_type = tile_types.floor
            if name and name in tile_types.minetestmapper_colors_tiles:
                tile_type = tile_types.minetestmapper_colors_tiles[name]
            self.tiles[x - x_min, z - z_min] = tile_type

    def load_map_from_database(self, database_path: str, table_name: str, x: int, y: int, z: int) -> None:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        query = f"SELECT * FROM {table_name} WHERE y = {y} AND x BETWEEN {x - 45} AND {x + 45} AND z BETWEEN {z - 45} AND {z + 45}"
        cursor.execute(query)
        result = cursor.fetchall()
        print(len(result))  # 打印行数
        print(len(result[0]))  # 打印列数
        # for row in result:
        #     print(row)
        # for row in result:
        #     x, y, z, tile_type = row
        #     self.tiles[x, z] = tile_type

        conn.close()
        return result


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def elevate_up(self) -> None:
        self.elevate += 1
        self.re_render(self.console)

    def elevate_down(self) -> None:
        self.elevate -= 1
        self.re_render(self.console)

    def set_elevate(self, elevate: int) -> None:
        self.elevate = elevate

    def get_elevate(self) -> int:
        return self.elevate

    def centerlocation_dxdz(self, dx: int, dy: int) -> None:
        self.location['x'] = self.location['x'] + dx
        self.location['z'] = self.location['z'] + dy
        self.re_render(self.console)

    def render(self, console: Console) -> None:
        self.console = console
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]

    def re_render(self, console: Console) -> None:
        self.map = self.load_map_from_database("./maps/blocks.db", "blocks", self.location['x'], self.elevate, self.location['z'])  # 从数据库加载地图数据

        x_min = min(row[0] for row in self.map)
        z_min = min(row[2] for row in self.map)
        print(x_min, z_min)  # 打印最小值

        
        for row in self.map:
            x, y, z, name, p1, p2 = row
            tile_type = tile_types.floor
            if name and name in tile_types.minetestmapper_colors_tiles:
                tile_type = tile_types.minetestmapper_colors_tiles[name]
            self.tiles[x - x_min, z - z_min] = tile_type

        self.render(console)