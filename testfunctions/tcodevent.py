import tcod

KEY_COMMANDS = {
    tcod.event.KeySym.UP: "move N",
    tcod.event.KeySym.DOWN: "move S",
    tcod.event.KeySym.LEFT: "move W",
    tcod.event.KeySym.RIGHT: "move E",
}

context = tcod.context.new()
while True:
    console = context.new_console()
    context.present(console, integer_scaling=True)
    for event in tcod.event.wait():
        context.convert_event(event)  # Adds tile coordinates to mouse events.
        match event:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown(sym) if sym in KEY_COMMANDS:
                print(f"Command: {KEY_COMMANDS[sym]}")
            case tcod.event.KeyDown(sym=sym, scancode=scancode, mod=mod, repeat=repeat):
                print(f"KeyDown: {sym=}, {scancode=}, {mod=}, {repeat=}")
            case tcod.event.MouseButtonDown(button=button, pixel=pixel, tile=tile):
                print(f"MouseButtonDown: {button=}, {pixel=}, {tile=}")
            case tcod.event.MouseMotion(pixel=pixel, pixel_motion=pixel_motion, tile=tile, tile_motion=tile_motion):
                print(f"MouseMotion: {pixel=}, {pixel_motion=}, {tile=}, {tile_motion=}")
            case tcod.event.JoystickButton(which=which, button=button, pressed=True):
                print(f"Pressed {button=} on controller {which}.")
            case tcod.event.JoystickButton(which=which, button=button, pressed=False):
                print(f"Released {button=} on controller {which}.")
            case tcod.event.Event() as event:
                print(event)  # Show any unhandled events.