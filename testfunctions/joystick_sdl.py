import tcod
from tcod.sdl.joystick import Joystick
import time
import ctypes

import tcod._libtcod.lib

def main():
    # 初始化 SDL 子系统
    tcod.lib.SDL_Init(tcod.lib.SDL_INIT_JOYSTICK)
    
    try:
        # 获取操纵杆数量
        joystick_count = tcod.lib.SDL_NumJoysticks()
        print(f'Number of joysticks: {joystick_count}')

        if joystick_count > 0:
            # 打开第一个操纵杆
            sdl_joystick_p = tcod.lib.SDL_JoystickOpen(0)
            joy = Joystick(sdl_joystick_p)
            print(f'Joystick name: {tcod.lib.SDL_JoystickName(sdl_joystick_p)}')
            joystick_guid = tcod.lib.SDL_JoystickGetGUID(sdl_joystick_p)
            print(joystick_guid)

            # 获取操纵杆的各项信息
            axes = tcod.lib.SDL_JoystickNumAxes(sdl_joystick_p)
            buttons = tcod.lib.SDL_JoystickNumButtons(sdl_joystick_p)
            print(f'Axes: {axes}, Buttons: {buttons}')
            
            # 游戏主循环
            while True:
                #button0 = tcod.lib.SDL_JoystickGetButton(sdl_joystick_p, 0)
                #print(joy.get_button(0))
                for event in tcod.event.wait():
                    if event.type == tcod.event.JoystickButton(which=0, button=0, type="pressed"):
                        print(f'Button {event.button} pressed')
                    elif event.type == tcod.event.JoystickButton(which=0, button=0, type="released"):
                        print(f'Button {event.button} released')
                    else:
                        print(event)

                    # match event:
                    #     case tcod.event.JoystickDevice(type="JOYDEVICEADDED", joystick=new_joystick):
                    #         print("JOYDEVICEADDED")
                    #     case tcod.event.JoystickDevice(type="JOYDEVICEREMOVED", joystick=joystick):
                    #         print("JOYDEVICEMOVED")
 
                # print(button0)
                time.sleep(0.1)  # 延迟以便于读取
        else:
            print('No joysticks connected.')

    finally:
        # 关闭操纵杆
        if joystick_count > 0:
            tcod.lib.SDL_JoystickClose(sdl_joystick_p)

        # 退出 SDL 子系统
        tcod.lib.SDL_Quit()

if __name__ == '__main__':
    main()
