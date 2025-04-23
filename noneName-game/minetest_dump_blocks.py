import miney
import time
import sqlite3

# 定义常量来模拟宏
SEARCH_RANGE = 50

# 初始化 Minetest 连接
mt = miney.Minetest()

# 初始化上一次的玩家位置
last_player_position = None

# 连接到 SQLite 数据库
conn = sqlite3.connect('./maps/blocks.db')
cursor = conn.cursor()

# 创建表格，使用 UNIQUE 约束确保 (x, y, z) 组合唯一
cursor.execute('''
CREATE TABLE IF NOT EXISTS blocks (
    x INTEGER,
    y INTEGER,
    z INTEGER,
    name TEXT,
    param1 TEXT,
    param2 TEXT,
    UNIQUE (x, y, z)
)
''')
conn.commit()
# 初始化mt.player[0]的position
# mt.player[0].position = {
#     'x': 256,
#     'y': 4,
#     'z': 256
# }




while True:
    try:
        # 获取玩家位置并取整
        player_position = mt.player[0].position
        player_position['x'] = int(player_position['x'])
        player_position['y'] = int(player_position['y'])
        player_position['z'] = int(player_position['z'])

        # 检查玩家位置是否改变
        if last_player_position is None or (
            player_position['x'] != last_player_position['x'] or
            player_position['y'] != last_player_position['y'] or
            player_position['z'] != last_player_position['z']
        ):
            print(player_position)

            # 定义搜索范围的两个端点
            # position_p1 = {
            #     'x': player_position['x'],
            #     'y': player_position['y'],
            #     'z': player_position['z']
            # }
            # position_p2 = {
            #     'x': player_position['x'] + SEARCH_RANGE-1,
            #     'y': player_position['y'] + SEARCH_RANGE-1,
            #     'z': player_position['z'] + SEARCH_RANGE-1
            # }
            position_p1 = {
                'x': 0,
                'y': 0,
                'z': 0
            }
            position_p2 = {
                'x': SEARCH_RANGE,
                'y': SEARCH_RANGE,
                'z': SEARCH_RANGE
            }
            # 一次性获取指定区域内的方块信息
            blocks = mt.node.get(position_p1, position_p2)

            new_data_count = 0
            print(len(blocks))  # 打印获取的方块数量
            for block in blocks:
                try:
                    # 插入数据到 SQLite 数据库，使用 INSERT OR IGNORE 避免重复插入
                    cursor.execute('''
                    INSERT OR IGNORE INTO blocks (x, y, z, name, param1, param2)
                    VALUES (?,?,?,?,?,?)
                    ''', (block['x'], block['y'], block['z'], block['name'], block['param1'], block['param2']))
                    if cursor.rowcount > 0:
                        new_data_count += 1
                except sqlite3.IntegrityError:
                    # 若违反唯一性约束，跳过该记录
                    continue
            conn.commit()

            if new_data_count > 0:
                print(f"新增数据数量: {new_data_count}")

            # 更新上一次的玩家位置
            last_player_position = player_position

        time.sleep(0.1)

    except Exception as e:
        print(f"发生错误: {e}")
        break

# 关闭数据库连接
conn.close()