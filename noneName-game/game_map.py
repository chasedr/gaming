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
        self.location = {'x': 0, 'z': 0}  # 位置坐标
        # self.tiles[30:70, 22] = tile_types.wall

        self.map = self.load_map_from_database("./maps/blocks.db", "blocks", self.location['x'], self.elevate, self.location['z'])  # 从数据库加载地图数据

        x_min = min(row[0] for row in self.map)
        z_min = min(row[2] for row in self.map)
        # print(x_min, z_min)  # 打印最小值

        
        for row in self.map:
            x, y, z, name, p1, p2 = row
            tile_type = tile_types.air
            if name and name in tile_types.minetestmapper_colors_tiles:
                tile_type = tile_types.minetestmapper_colors_tiles[name]
            self.tiles[x - x_min, z - z_min] = tile_type

    def load_map_from_database(self, database_path: str, table_name: str, x: int, y: int, z: int) -> list:
        try:
            # 连接到数据库
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()

            # 使用参数化查询，避免SQL注入
            query = f"SELECT * FROM {table_name} WHERE y =? AND x BETWEEN? AND? AND z BETWEEN? AND?"
            params = (y, x, x + 70, z, z + 40)
            cursor.execute(query, params)

            # 获取查询结果
            result = cursor.fetchall()

            # 打印结果的行数和列数
            if result:
                print(len(result), len(result[0]))
            else:
                print("No results found.")

            # 关闭游标和连接
            cursor.close()
            conn.close()

            return result

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []


    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def elevate_up(self) -> None:
        # print(self.elevate)
        self.elevate += 1
        self.re_render(self.console)

    def elevate_down(self) -> None:
        # print(self.elevate)
        self.elevate -= 1
        self.re_render(self.console)

    def set_elevate(self, elevate: int) -> None:
        self.elevate = elevate

    def get_elevate(self) -> int:
        return self.elevate

    def get_location_name(self, x: int, z: int) -> str:
        for row in self.map:
            sx, sy, sz, sname, sp1, sp2 = row
            if sx == x and sz == z and sy == self.elevate:
                return sname
                
    def centerlocation_dxdz(self, dx: int, dz: int) -> None:
        print(self.location['x'], self.location['z'], dx, dz)
        self.location['x'] = self.location['x'] + dx
        self.location['z'] = self.location['z'] + dz
        self.re_render(self.console)

    def render(self, console: Console) -> None:
        self.console = console
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]

    def re_render(self, console: Console) -> None:
        self.map = self.load_map_from_database("./maps/blocks.db", "blocks", self.location['x'], self.elevate, self.location['z'])  # 从数据库加载地图数据

        # print(self.map[:5])
        print("x,z,y", self.location['x'], self.location['z'], self.elevate)
        
        if self.map:
            x_min = min(row[0] for row in self.map)
            z_min = min(row[2] for row in self.map)
            print("x_min", x_min, "z_min", z_min)  # 打印最小值

            for row in self.map:
                x, y, z, name, p1, p2 = row
                tile_type = tile_types.air
                if name and name in tile_types.minetestmapper_colors_tiles:
                    tile_type = tile_types.minetestmapper_colors_tiles[name]
                self.tiles[x - x_min, z - z_min] = tile_type

            self.render(console)