import miney
import time

# 定义常量来模拟宏
SEARCH_RANGE = 20

# 初始化 Minetest 连接
mt = miney.Minetest()

# 初始化mt.player[0]的position
# mt.player[0].position = {
#     'x': 232,
#     'y': 0,
#     'z': 265
# }

player_position = mt.player[0].position
print(player_position)

player_position['x'] = 0
player_position['y'] = 30
player_position['z'] = 0

mt.player[0].position = player_position


# for y in range(-30, 30, 10):
#     player_position['y'] = y
#     for x in range(-50, 50, 20):
#         player_position['x'] = x
#         for z in range(-50, 50, 20):
#             player_position['z'] = z
#             mt.player[0].position = player_position
#             time.sleep(0.2)
#             print(y, x, z)
