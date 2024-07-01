import pygame
import ctypes
from time import sleep

# 初始化 pygame
pygame.init()
pygame.joystick.init()

# 打开第一个游戏手柄
joystick = pygame.joystick.Joystick(0)
joystick.init()

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
sleep(1)  # 震动1秒
set_vibration(0, 0)  # 停止震动

# 退出 pygame
pygame.quit()
