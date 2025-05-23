#!/usr/bin/env python3
import tcod

from engine import Engine
from entity import Entity , Person
from game_map import GameMap
from input_handlers import EventHandler


def main() -> None:
    screen_width = 80
    screen_height = 60

    map_width = 80
    map_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    game_map = GameMap(map_width, map_height)

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    Alice = Person(int(screen_width / 2), int(screen_height / 3), "@", (255, 0, 0), "Alice", game_map=game_map)
    entities = {npc, player, Alice}

    Alice.start()
    

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait(timeout=1)

            engine.handle_events(events)

            


if __name__ == "__main__":
    main()
