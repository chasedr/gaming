import numpy as np
import wave
import pygame
import os
import multiprocessing
import cv2
import ffmpeg
from pydub import AudioSegment

# 提取视频文件中的音频并转换为 PCM 格式
def extract_and_convert_audio(video_path, audio_output_path):
    stream = ffmpeg.input(video_path)
    stream = ffmpeg.output(stream, audio_output_path)
    ffmpeg.run(stream)
    sound = AudioSegment.from_file(audio_output_path, format="wav")
    sound = sound.set_channels(2).set_frame_rate(44100)
    sound.export(audio_output_path, format="wav", codec="pcm_s16le")

# 窗口显示图片的函数
def show_image(image_path):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0" # 设置第一个窗口的位置
    pygame.init()
    size = width, height = 640, 360
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Image Window')

    # 加载图片
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (width, height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))
        pygame.display.flip()

    pygame.quit()

# 窗口显示音频波形的函数
def show_waveform(audio_path):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "640,0" # 设置第二个窗口的位置

    def load_wave_and_raw_data(filename):
        with wave.open(filename, 'r') as wf:
            frames = wf.readframes(wf.getnframes())
            wave_data = np.frombuffer(frames, dtype=np.int16)
            wave_data = wave_data.astype(np.float32) / 32768.0  # 归一化

        return wave_data

    wave_data = load_wave_and_raw_data(audio_path)

    pygame.init()
    size = width, height = 640, 360
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Waveform Window')

    clock = pygame.time.Clock()

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)

    def draw_waveform(screen, wave_data, width, height):
        middle_y = height // 2
        scale_x = len(wave_data) / width
        scale_y = middle_y

        for x in range(width):
            index = int(x * scale_x)
            if index < len(wave_data):
                y = int(wave_data[index] * scale_y)
                pygame.draw.line(screen, (0, 255, 0), (x, middle_y - y), (x, middle_y + y))

    running = True
    playing = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not playing:
                    pygame.mixer.music.play()
                    playing = True
                else:
                    pygame.mixer.music.stop()
                    playing = False

        screen.fill((0, 0, 0))
        draw_waveform(screen, wave_data, width, height)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

# 窗口显示单词和音标的函数
def show_text(word, phonetic):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "1280,0" # 设置第三个窗口的位置
    pygame.init()
    size = width, height = 640, 360
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Text Window')

    # 定义字体
    font = pygame.font.SysFont('Arial', 36)
    phonetic_font = pygame.font.SysFont('Arial', 28)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # 白色背景

        # 绘制单词
        word_surface = font.render(word, True, (0, 0, 0))
        word_rect = word_surface.get_rect(center=(width // 2, height // 3))
        screen.blit(word_surface, word_rect)

        # 绘制音标
        phonetic_surface = phonetic_font.render(phonetic, True, (0, 0, 0))
        phonetic_rect = phonetic_surface.get_rect(center=(width // 2, 2 * height // 3))
        screen.blit(phonetic_surface, phonetic_rect)

        pygame.display.flip()

    pygame.quit()

# 窗口播放视频的函数
def show_video(video_path):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,360" # 设置第四个窗口的位置

    audio_temp_path = 'temp_audio.wav'
    extract_and_convert_audio(video_path, audio_temp_path)

    pygame.init()
    size = width, height = 640, 360
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Video Window')

    cap = cv2.VideoCapture(video_path)
    clock = pygame.time.Clock()
    running = True
    playing = False
    playback_started = False

    pygame.mixer.init()
    pygame.mixer.music.load(audio_temp_path)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not playing:
                    pygame.mixer.music.play()
                    playing = True
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 从头开始播放视频
                    playback_started = True
                else:
                    pygame.mixer.music.stop()
                    playing = False

        if playing:
            ret, frame = cap.read()
            if not ret:
                pygame.mixer.music.stop()
                playing = False
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重置视频到开头
                playback_started = False
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (width, height))
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)

            screen.blit(frame, (0, 0))
            pygame.display.flip()

        clock.tick(30)

    cap.release()
    pygame.quit()

# 窗口用于输入文字并显示系统回应消息
def input_text_window():
    os.environ['SDL_VIDEO_WINDOW_POS'] = '640,360'  # 设置第五个窗口的位置

    pygame.init()
    size = width, height = 640, 360
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Input Text Window')

    font = pygame.font.SysFont('Arial', 24)
    input_text = ''
    response_text = 'System: Waiting for input...'
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    response_text = f'System: You typed "{input_text}"'
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill((255, 255, 255))  # 白色背景
        input_surface = font.render(f'Input: {input_text}', True, (0, 0, 0))
        response_surface = font.render(response_text, True, (0, 0, 0))
        screen.blit(input_surface, (10, 10))
        screen.blit(response_surface, (10, 50))
        pygame.display.flip()

    pygame.quit()

# 窗口显示单词列表
def show_word_list(word_list, position):
    os.environ['SDL_VIDEO_WINDOW_POS'] = position

    pygame.init()
    size = width, height = 640, 360
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Word List Window')

    font = pygame.font.SysFont('Arial', 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # 白色背景
        for i, word in enumerate(word_list):
            word_surface = font.render(f'{i + 1}. {word}', True, (0, 0, 0))
            screen.blit(word_surface, (10, 10 + i * 30))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    image_path = 'temp.jpg'  # 替换为你的图片路径
    audio_path = 'temp_converted.wav'  # 替换为你的音频路径
    word = 'Apple'  # 替换为你想显示的单词
    phonetic = '[həˈləʊ]'  # 替换为你想显示的音标
    video_path = 'temp.mp4'  # 替换为你的视频路径
    word_list1 = ['apple', 'banana', 'cherry']  # 替换为你的单词列表1
    word_list2 = ['dog', 'elephant', 'frog']  # 替换为你的单词列表2

    p1 = multiprocessing.Process(target=show_image, args=(image_path,))
    p2 = multiprocessing.Process(target=show_waveform, args=(audio_path,))
    p3 = multiprocessing.Process(target=show_text, args=(word, phonetic,))
    p4 = multiprocessing.Process(target=show_video, args=(video_path,))
    p5 = multiprocessing.Process(target=input_text_window)
    p6 = multiprocessing.Process(target=show_word_list, args=(word_list1, '1280,360'))
    p7 = multiprocessing.Process(target=show_word_list, args=(word_list2, '0,720'))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
