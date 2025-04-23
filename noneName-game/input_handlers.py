from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction, ElevateAction, GameMapCenterMove


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)
        elif key == tcod.event.K_w:
            action = GameMapCenterMove(dx=0, dz=1)
        elif key == tcod.event.K_s:
            action = GameMapCenterMove(dx=0, dz=-1)
        elif key == tcod.event.K_a:
            action = GameMapCenterMove(dx=1, dz=0)
        elif key == tcod.event.K_d:
            action = GameMapCenterMove(dx=-1, dz=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> Optional[Action]:
        # Handle mouse motion events if needed
        
        return None

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        # Handle mouse button down events if needed
        
        print(f"Mouse button {event.button} pressed at {event.position}")
        return None

    def ev_mousebuttonup(self, event: tcod.event.MouseButtonUp) -> Optional[Action]:
        # Handle mouse button up events if needed
        print(f"Mouse button {event.button} released at {event.position}")
        return None

    def ev_mousewheel(self, event: tcod.event.MouseWheel) -> Optional[Action]:
        # Handle mouse wheel events if needed
        print(event)
        print(f"Mouse wheel scrolled {event.y} at {event.x}, {event.y}")
        action = ElevateAction(event.y)
        return action