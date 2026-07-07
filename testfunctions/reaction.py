import time
import random

def reaction_test():
    print("⏱️ 反应速度测试")
    input("准备好后按回车开始...")
    wait_time = random.uniform(2, 5)
    time.sleep(wait_time)
    start = time.perf_counter()
    input("⚡ 现在按回车！")
    elapsed = (time.perf_counter() - start) * 1000
    print(f"你的反应时间：{elapsed:.0f} 毫秒")
    if elapsed < 200:
        print("🏆 神级反应！")
    elif elapsed < 300:
        print("⭐ 非常优秀")
    elif elapsed < 400:
        print("👍 不错哦")
    else:
        print("🐢 需要多练习～")

if __name__ == "__main__":
    reaction_test()