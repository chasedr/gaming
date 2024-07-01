import tcod

# 游戏设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
LIMIT_FPS = 20

# 颜色定义
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_TANK_1 = (0, 255, 0)
COLOR_TANK_2 = (0, 0, 255)
COLOR_BULLET = (255, 0, 0)

# 坦克类
class Tank:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.tile = tile

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, console):
        console.tiles_rgb[self.x, self.y] = self.tile

# 子弹类
class Bullet:
    def __init__(self, x, y, dx, dy, tile):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.tile = tile

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, console):
        console.tiles_rgb[self.x, self.y] = self.tile

# 初始化游戏
def main():
    # 加载 tileset
    tileset = tcod.tileset.load_tilesheet('dejavu10x10_gs_tc.png', 16, 16, tcod.tileset.CHARMAP_TCOD)

    with tcod.context.new(columns=SCREEN_WIDTH, rows=SCREEN_HEIGHT, tileset=tileset, title="Tank Battle", vsync=True) as context:
        console = tcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")

        tank1_tile = (ord('T'), COLOR_TANK_1, COLOR_BLACK)
        tank2_tile = (ord('T'), COLOR_TANK_2, COLOR_BLACK)
        bullet_tile = (ord('*'), COLOR_BULLET, COLOR_BLACK)

        tank1 = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, tank1_tile)
        tank2 = Tank(SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2, tank2_tile)
        bullets = []

        while True:
            console.clear()

            # 处理输入
            for event in tcod.event.wait():
                context.convert_event(event)

                if event.type == "QUIT":
                    raise SystemExit()
                elif event.type == "KEYDOWN":
                    print(event.sym)

                    if event.sym == tcod.event.KeySym.ESCAPE:
                        raise SystemExit()
                    elif event.sym == tcod.event.KeySym.UP:
                        tank1.move(0, -1)
                    elif event.sym == tcod.event.KeySym.DOWN:
                        tank1.move(0, 1)
                    elif event.sym == tcod.event.KeySym.LEFT:
                        tank1.move(-1, 0)
                    elif event.sym == tcod.event.KeySym.RIGHT:
                        tank1.move(1, 0)
                    elif event.sym == tcod.event.KeySym.SPACE:
                        bullets.append(Bullet(tank1.x, tank1.y, 0, -1, bullet_tile))
                    
                    # 控制第二辆坦克，使用WASD键和F键发射子弹
                    elif event.sym == tcod.event.KeySym.w:
                        tank2.move(0, -1)
                    elif event.sym == tcod.event.KeySym.s:
                        tank2.move(0, 1)
                    elif event.sym == tcod.event.KeySym.a:
                        tank2.move(-1, 0)
                    elif event.sym == tcod.event.KeySym.d:
                        tank2.move(1, 0)
                    elif event.sym == tcod.event.KeySym.f:
                        bullets.append(Bullet(tank2.x, tank2.y, 0, -1, bullet_tile))

            # 更新游戏状态
            for bullet in bullets:
                bullet.update()

            # 渲染游戏
            tank1.draw(console)
            tank2.draw(console)
            for bullet in bullets:
                bullet.draw(console)

            context.present(console)

if __name__ == '__main__':
    main()
