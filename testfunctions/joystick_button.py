import pygame
import sys
import ctypes
import time

# 初始化 pygame
pygame.init()
pygame.joystick.init()

# 检查是否有连接的手柄
if pygame.joystick.get_count() == 0:
    print("未检测到任何手柄")
    sys.exit()

# 打开第一个手柄
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"已连接的手柄: {joystick.get_name()}")

# 获取手柄的按钮数量
num_buttons = joystick.get_numbuttons()


# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed")
        elif event.type == pygame.JOYBUTTONUP:
            print(f"Button {event.button} released")
        elif event.type == pygame.JOYAXISMOTION:
            print(f"Axis {event.axis} value: {joystick.get_axis(event.axis)}")
        elif event.type == pygame.JOYHATMOTION:
            print(f"Hat {event.hat} value: {joystick.get_hat(event.hat)}")

pygame.quit()
