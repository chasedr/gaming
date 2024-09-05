import pygame
import math
import sys

# 初始设置
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Arrow Rectangle Game")
clock = pygame.time.Clock()

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# 定义长方形和箭头属性
rect_width = 20  # 长方形宽度
rect_height = 10  # 长方形高度
arrow_length = rect_height / 2
arrow_angle = 0  # 初始角度
rect_x, rect_y = 400, 300  # 长方形初始中心点
initial_rect_x, initial_rect_y = rect_x, rect_y
rect_speed = 5

# 墙壁属性
walls = [
    pygame.Rect(100, 100, 600, 10),   # 水平墙
    pygame.Rect(100, 200, 10, 400),   # 垂直墙
    pygame.Rect(700, 200, 10, 400)    # 垂直墙
]

# 子弹属性
bullet_speed = 7
bullets = []

# 计算旋转后的点
def rotate_point(px, py, cx, cy, angle):
    s = math.sin(angle)
    c = math.cos(angle)
    
    # 平移点到原点
    px -= cx
    py -= cy
    
    # 旋转点
    xnew = px * c - py * s
    ynew = px * s + py * c

    # 平移点回原位置
    px = xnew + cx
    py = ynew + cy
    return px, py

# 计算反射方向
def reflect(bullet_dx, bullet_dy, normal_x, normal_y):
    dot_product = (bullet_dx * normal_x + bullet_dy * normal_y) * 2
    reflect_dx = bullet_dx - dot_product * normal_x
    reflect_dy = bullet_dy - dot_product * normal_y
    return reflect_dx, reflect_dy

# 检查坦克是否与墙壁碰撞
def check_collision_with_walls(rect_x, rect_y, rect_width, rect_height, angle):
    rect_points = [
        (rect_x - rect_width / 2, rect_y - rect_height / 2),
        (rect_x + rect_width / 2, rect_y - rect_height / 2),
        (rect_x + rect_width / 2, rect_y + rect_height / 2),
        (rect_x - rect_width / 2, rect_y + rect_height / 2)
    ]
    rotated_rect_points = [rotate_point(px, py, rect_x, rect_y, angle) for px, py in rect_points]
    rect_polygon = pygame.draw.polygon(screen, RED, rotated_rect_points, 1)
    
    for wall in walls:
        if rect_polygon.colliderect(wall):
            return True
    return False

# 检查子弹是否与长方形碰撞
def check_bullet_collision_with_rect(bullet_x, bullet_y, rect_x, rect_y, rect_width, rect_height, angle):
    rect_points = [
        (rect_x - rect_width / 2, rect_y - rect_height / 2),
        (rect_x + rect_width / 2, rect_y - rect_height / 2),
        (rect_x + rect_width / 2, rect_y + rect_height / 2),
        (rect_x - rect_width / 2, rect_y + rect_height / 2)
    ]
    rotated_rect_points = [rotate_point(px, py, rect_x, rect_y, angle) for px, py in rect_points]
    rect_polygon = pygame.Rect(min([p[0] for p in rotated_rect_points]), min([p[1] for p in rotated_rect_points]), 
                               max([p[0] for p in rotated_rect_points]) - min([p[0] for p in rotated_rect_points]), 
                               max([p[1] for p in rotated_rect_points]) - min([p[1] for p in rotated_rect_points]))
    
    if rect_polygon.collidepoint(bullet_x, bullet_y):
        return True
    return False

# 绘制长方形和箭头
def draw_rotated_rect_arrow(screen, rect_x, rect_y, rect_width, rect_height, arrow_angle):
    # 矩形点
    rect_points = [
        (rect_x - rect_width / 2, rect_y - rect_height / 2),
        (rect_x + rect_width / 2, rect_y - rect_height / 2),
        (rect_x + rect_width / 2, rect_y + rect_height / 2),
        (rect_x - rect_width / 2, rect_y + rect_height / 2)
    ]
    
    # 旋转矩形点
    rotated_rect_points = [rotate_point(px, py, rect_x, rect_y, arrow_angle) for px, py in rect_points]
    
    # 绘制旋转后的矩形
    pygame.draw.polygon(screen, RED, rotated_rect_points)
    
    # 箭头起点和终点
    center_x = rect_x
    center_y = rect_y
    arrow_end_x = center_x + arrow_length * math.cos(arrow_angle)
    arrow_end_y = center_y + arrow_length * math.sin(arrow_angle)
    
    # 绘制箭头
    pygame.draw.line(screen, BLACK, (center_x, center_y), (arrow_end_x, arrow_end_y), 3)

# 游戏循环
running = True
while running:
    # 退出事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 发射子弹
                bullet_x = rect_x+rect_width*math.cos(arrow_angle)
                bullet_y = rect_y+rect_height*math.sin(arrow_angle)
                bullet_dx = bullet_speed * math.cos(arrow_angle)
                bullet_dy = bullet_speed * math.sin(arrow_angle)
                bullets.append((bullet_x, bullet_y, bullet_dx, bullet_dy, 0))  # 子弹初始反弹次数为0
    
    # 键盘事件处理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        arrow_angle -= 0.1  # 调整箭头方向和长方体一起旋转
    if keys[pygame.K_RIGHT]:
        arrow_angle += 0.1  # 调整箭头方向和长方体一起旋转
    
    # 移动坦克
    if keys[pygame.K_UP]:
        new_x = rect_x + rect_speed * math.cos(arrow_angle)
        new_y = rect_y + rect_speed * math.sin(arrow_angle)
        if not check_collision_with_walls(new_x, new_y, rect_width, rect_height, arrow_angle):
            rect_x = new_x
            rect_y = new_y
    if keys[pygame.K_DOWN]:
        new_x = rect_x - rect_speed * math.cos(arrow_angle)
        new_y = rect_y - rect_speed * math.sin(arrow_angle)
        if not check_collision_with_walls(new_x, new_y, rect_width, rect_height, arrow_angle):
            rect_x = new_x
            rect_y = new_y
    
    # 更新子弹位置
    new_bullets = []
    for bullet in bullets:
        bullet_x, bullet_y, bullet_dx, bullet_dy, reflect_count = bullet
        bullet_x += bullet_dx
        bullet_y += bullet_dy
        bullet_rect = pygame.Rect(bullet_x - 1, bullet_y - 1, 2, 2)  # 子弹的矩形表示，用于碰撞检测
        
        # 检查子弹是否与长方形碰撞
        if check_bullet_collision_with_rect(bullet_x, bullet_y, rect_x, rect_y, rect_width, rect_height, arrow_angle):
            # 将长方形移回初始位置
            rect_x, rect_y = initial_rect_x, initial_rect_y
            continue
        
        # 检查子弹是否与任何墙壁碰撞
        collision = False
        for wall in walls:
            if bullet_rect.colliderect(wall):
                # 检测垂直或水平墙碰撞，并相应反射子弹
                if wall.width > wall.height:  # 水平墙
                    bullet_dx, bullet_dy = reflect(bullet_dx, bullet_dy, 0, 1)
                else:  # 垂直墙
                    bullet_dx, bullet_dy = reflect(bullet_dx, bullet_dy, 1, 0)
                reflect_count += 1
                collision = True
                break
        
        if reflect_count < 3 and 0 <= bullet_x <= 800 and 0 <= bullet_y <= 600:
            new_bullets.append((bullet_x, bullet_y, bullet_dx, bullet_dy, reflect_count))
    bullets = new_bullets

    # 清除屏幕
    screen.fill(WHITE)
    
    # 绘制旋转的长方形和箭头
    draw_rotated_rect_arrow(screen, rect_x, rect_y, rect_width, rect_height, arrow_angle)

    # 绘制墙壁
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)

    # 绘制子弹
    for bullet in bullets:
        pygame.draw.circle(screen, BLACK, (int(bullet[0]), int(bullet[1])), 3)
    
    # 更新显示
    pygame.display.flip()
    clock.tick(30)

# 退出
pygame.quit()
sys.exit()
