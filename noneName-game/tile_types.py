from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool_),  # True if this tile can be walked over.
        ("transparent", np.bool_),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark), dtype=tile_dt)

def parse_color_file(file_path):
    colors = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()[2:]  # Skip the first two lines
        for line in lines:
            line = line.strip()
            # print(line)  # Print each line for debugging
            if line:
                try:
                    key, r, g, b = line.split()
                    colors[key] = (int(r), int(g), int(b))
                except ValueError:
                    continue
    return colors

color_file_path = "./maps/colors.txt"  # Replace with the actual file path
parsed_colors = parse_color_file(color_file_path)
print(len(parsed_colors))  # Print the parsed colors
print(type(parsed_colors)) 


# Combine parsed colors with new_tile
for key, color in parsed_colors.items():
    tile = new_tile(walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), color))
    globals()[key] = tile
minetestmapper_colors_tiles = globals().copy()



floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
)
