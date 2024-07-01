import tcod
import time
import ctypes
from tcod.sdl.joystick import GameController

import tcod._libtcod.lib
from cffi import FFI
ffi = FFI()





def main():
    # 初始化 SDL 子系统
    tcod.lib.SDL_Init(tcod.lib.SDL_INIT_GAMECONTROLLER)
    # tcod.lib.SDL_Init(tcod.lib.SDL_INIT_EVENTS)
    # tcod.lib.SDL_Init(tcod.lib.SDL_INIT_JOYSTICK)
    
    try:
        # 获取操纵杆数量
        joystick_count = tcod.lib.SDL_NumJoysticks()
        print(f'Number of joysticks: {joystick_count}')

        if joystick_count > 0:
            # 打开第一个操纵杆
            sdl_controller_p = tcod.lib.SDL_GameControllerOpen(0)
            gamecontroller = GameController(sdl_controller_p)
            # 遍历字符串
            # controller_name = ctypes.string_at(tcod.lib.SDL_GameControllerName(sdl_controller_p))
            # print(controller_name)
            controllername = tcod.lib.SDL_GameControllerName(sdl_controller_p)
            controller_name = ffi.string(controllername).decode('utf-8')
            print('Joystick name:', controller_name)  # 输出控制器名称

            joystick_guid = tcod.lib.SDL_GameControllerGetSerial(sdl_controller_p)
            print(joystick_guid)



            # 尝试加载不同版本的 XInput DLL 文件
            xinput_dll_names = ['xinput1_4.dll', 'xinput1_3.dll', 'xinput9_1_0.dll']

            for dll_name in xinput_dll_names:
                try:
                    XInput = ctypes.windll.LoadLibrary(dll_name)
                    break
                except OSError:
                    pass
            else:
                raise OSError("Could not load any XInput DLL")

            class XInputVibration(ctypes.Structure):
                _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                            ("wRightMotorSpeed", ctypes.c_ushort)]

            def set_vibration(left_motor, right_motor):
                vibration = XInputVibration(left_motor, right_motor)
                XInput.XInputSetState(0, ctypes.byref(vibration))

            # 设置震动：左马达和右马达的速度范围是0到65535
            set_vibration(40000, 0)
            time.sleep(1)  # 震动1秒
            set_vibration(0, 0)  # 停止震动

            # 获取操纵杆的各项信息
            # axes = tcod.lib.SDL_JoystickNumAxes(sdl_joystick_p)
            # buttons = tcod.lib.SDL_JoystickNumButtons(sdl_joystick_p)
            # print(f'Axes: {axes}, Buttons: {buttons}')
            
            context = tcod.context.new()
            # 游戏主循环
            while True:
                console = context.new_console()
                context.present(console, integer_scaling=True)
                #button0 = tcod.lib.SDL_JoystickGetButton(sdl_joystick_p, 0)
                #print(joy.get_button(0))
                for event in tcod.event.wait():
                    context.convert_event(event)  # Adds tile coordinates to mouse events.
                    if event.type == "CONTROLLERBUTTONUP":
                        print(f'Button {event.button} pressed')
                        set_vibration(40000, 0)
                        time.sleep(0.1)  # 震动1秒
                        set_vibration(0, 0)  # 停止震动
                    elif event.type == tcod.event.ControllerButton(which=0, button=0, type="CONTROLLERBUTTONDOWN", pressed=True):
                        print(f'Button {event.button} pressed')
                        set_vibration(40000, 0)
                        time.sleep(1)  # 震动1秒
                        set_vibration(0, 0)  # 停止震动
                    elif event.type == tcod.event.ControllerButton(which=0, button=0, type="released", pressed=False):
                        print(f'Button {event.button} released')
                    else:
                        print(event)

                    match event:
                        case tcod.event.Quit():
                            raise SystemExit()
                    # match event:
                    #     case tcod.event.JoystickDevice(type="JOYDEVICEADDED", joystick=new_joystick):
                    #         print("JOYDEVICEADDED")
                    #     case tcod.event.JoystickDevice(type="JOYDEVICEREMOVED", joystick=joystick):
                    #         print("JOYDEVICEMOVED")
 
                # print(button0)
                # time.sleep(0.1)  # 延迟以便于读取
        else:
            print('No joysticks connected.')

    finally:
        # 关闭操纵杆
        if joystick_count > 0:
            tcod.lib.SDL_GameControllerClose(sdl_controller_p)

        # 退出 SDL 子系统
        tcod.lib.SDL_Quit()

if __name__ == '__main__':
    main()
