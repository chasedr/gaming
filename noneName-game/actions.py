from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        entity.stop()
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        entity.move(self.dx, self.dy)

class ElevateAction(Action):
    def __init__(self, elevate_direction: int):
        super().__init__()
        self.elevate_direction = elevate_direction

    def perform(self, engine: Engine, entity: Entity) -> None:
        if(self.elevate_direction > 0):
            engine.game_map.elevate_up()
        elif(self.elevate_direction < 0):
            engine.game_map.elevate_down()

class GameMapCenterMove(Action):
    def __init__(self, dx: int, dz: int):
        super().__init__()
        self.dx = dx
        self.dz = dz

    def perform(self, engine: Engine, entity: Entity) -> None:
        engine.game_map.centerlocation_dxdz(self.dx, self.dz)