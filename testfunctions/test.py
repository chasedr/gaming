import pygame

# 初始化 Pygame
pygame.init()

# 设置窗口初始大小和标题
initial_window_size = (800, 600)
screen = pygame.display.set_mode(initial_window_size, pygame.RESIZABLE)
pygame.display.set_caption("Resizable Window Example")

# 定义颜色
background_color = (255, 255, 255)
border_color = (0, 0, 0)
inner_color = (0, 128, 255)

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            new_width, new_height = event.w, event.h
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        
    # 获取当前窗口大小
    window_width, window_height = screen.get_size()

    # 填充背景色
    screen.fill(background_color)

    # 绘制一个居中的矩形，尺寸根据窗口大小动态调整
    border_width = 5
    rect_width, rect_height = window_width // 2, window_height // 2
    rect_x = (window_width - rect_width) // 2
    rect_y = (window_height - rect_height) // 2
    rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    # 绘制边框
    pygame.draw.rect(screen, border_color, rect, border_width)

    # 绘制内部颜色
    inner_rect = rect.inflate(-2*border_width, -2*border_width)
    pygame.draw.rect(screen, inner_color, inner_rect)

    # 更新显示
    pygame.display.flip()

pygame.quit()
