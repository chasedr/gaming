import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

# 创建并连接到 SQLite 数据库
conn = sqlite3.connect('graph.db')

# 创建游标对象
cur = conn.cursor()

# 创建节点和边的表
cur.execute('''CREATE TABLE IF NOT EXISTS nodes (id INTEGER PRIMARY KEY, label TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS edges (source INTEGER, target INTEGER, weight REAL)''')

# 插入节点
cur.execute("INSERT INTO nodes (label) VALUES ('A')")
cur.execute("INSERT INTO nodes (label) VALUES ('B')")
cur.execute("INSERT INTO nodes (label) VALUES ('C')")

# 插入边
cur.execute("INSERT INTO edges (source, target, weight) VALUES (1, 2, 1.0)")
cur.execute("INSERT INTO edges (source, target, weight) VALUES (2, 3, 2.0)")
cur.execute("INSERT INTO edges (source, target, weight) VALUES (3, 1, 3.0)")

# 提交事务并关闭连接
conn.commit()
cur.close()

# 读取节点和边，构建图
def create_graph_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    G = nx.Graph()

    # 读取节点
    cur.execute("SELECT id, label FROM nodes")
    nodes = cur.fetchall()
    for node in nodes:
        G.add_node(node[0], label=node[1])

    # 读取边
    cur.execute("SELECT source, target, weight FROM edges")
    edges = cur.fetchall()
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])

    # 关闭连接
    cur.close()
    conn.close()

    return G

# 从数据库中构建图
G = create_graph_from_db('graph.db')

# 可视化图
pos = nx.spring_layout(G)  # 节点布局
labels = nx.get_node_attributes(G, 'label')
weights = nx.get_edge_attributes(G, 'weight')

nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=2000, font_size=16)
nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)

plt.show()
