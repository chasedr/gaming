import random
import time
import sys
import os

# ---------- 音乐模块（使用 pygame.mixer）----------
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False
    print("⚠️ 未安装 pygame，无法播放音乐。请运行: pip install pygame")
except Exception as e:
    SOUND_AVAILABLE = False
    print(f"⚠️ 音频初始化失败: {e}")

def play_sound(sound_id):
    """播放编号为 sound_id 的 WAV 文件，播放前强制停止所有声音。"""
    if not SOUND_AVAILABLE:
        return
    try:
        filename = f"{sound_id}.wav"
        if os.path.exists(filename):
            pygame.mixer.stop()          # 停止所有正在播放的声音
            sound = pygame.mixer.Sound(filename)
            sound.play()
    except Exception:
        pass

# ---------- 跨平台单字符输入 ----------
def getch():
    """返回用户按下的单个字符，不等待回车。"""
    if sys.platform == 'win32':
        import msvcrt
        return msvcrt.getch().decode('utf-8', errors='ignore')
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

# ---------- 游戏主逻辑 ----------
def rock_paper_scissors():
    choices = ["石头", "剪刀", "布"]
    win_rules = {"石头": "剪刀", "剪刀": "布", "布": "石头"}

    score_player = 0
    score_computer = 0

    print("✊ 极速石头剪刀布 · 音效版 ✊")
    print("规则：电脑出拳后，你必须在 100 毫秒内按下 1(石头) 2(剪刀) 3(布)")
    print("按 q 随时退出\n")

    while True:
        input("按回车键准备开始...")
        play_sound(1)  # 准备音效

        # 倒计时 3 秒，每秒播放 1 号音效（新音效会打断前一个）
        for i in range(3, 0, -1):
            print(i)
            play_sound(1)  # 每一声倒计时播放
            time.sleep(1)

        print("出拳！")
        play_sound(2)  # 电脑出拳音效

        # 电脑出拳
        computer_choice = random.choice(choices)
        t1 = time.perf_counter()          # 计时起点
        print(f"电脑出了：{computer_choice}")

        # 提示并等待按键
        print("你的选择 (1-石头 2-剪刀 3-布，q退出): ", end='', flush=True)
        key = getch()                     # 阻塞直到按键
        t2 = time.perf_counter()
        elapsed_ms = (t2 - t1) * 1000

        # 处理按键
        if key.lower() == 'q':
            play_sound(9)  # 退出音效
            print(f"\n最终比分：你 {score_player} - {score_computer} 电脑")
            break

        if key not in ['1', '2', '3']:
            print(f"\n❌ 无效按键 '{key}'，本轮作废")
            play_sound(4)  # 无效按键音效
            print()
            continue

        # 检查是否超时
        if elapsed_ms > 100:
            print(f"⏰ 超时！用时 {elapsed_ms:.0f}ms（要求 ≤100ms），本轮作废")
            play_sound(8)  # 超时音效
            print()
            continue

        # 有效输入，判定胜负
        player_choice = choices[int(key) - 1]
        print(f"\n你的选择：{player_choice}")   # 回显按键
        play_sound(3)  # 有效按键音效

        # 胜负判定
        if player_choice == computer_choice:
            print("🤝 平局")
            play_sound(7)  # 平局音效
        elif win_rules[player_choice] == computer_choice:
            print("🎉 你赢了！")
            play_sound(5)  # 胜利音效
            score_player += 1
        else:
            print("💻 电脑赢了！")
            play_sound(6)  # 失败音效
            score_computer += 1

        print(f"当前比分：你 {score_player} - {score_computer} 电脑\n")

if __name__ == "__main__":
    rock_paper_scissors()