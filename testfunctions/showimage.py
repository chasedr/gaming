import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口尺寸
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Display Image')

# 加载图片
image_path = 'OIP.jpg'  # 指定你的图片文件路径
image = pygame.image.load(image_path)

# 获取图片尺寸
image_rect = image.get_rect()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清屏
    screen.fill((0, 0, 0))

    # 绘制图片
    screen.blit(image, image_rect)

    # 更新屏幕
    pygame.display.flip()

# 退出Pygame
pygame.quit()
sys.exit()
