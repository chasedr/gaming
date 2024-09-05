import numpy as np
import wave
import pygame
from pygame.locals import *
from pydub import AudioSegment

def load_wave_and_raw_data(filename):
    # Load the audio file using pydub, then convert to raw data
    audio = AudioSegment.from_file(filename)
    audio = audio.set_channels(1) # Make sure it's mono
    raw_data = np.array(audio.get_array_of_samples())

    # Save the audio in wav format for Pygame playback
    temp_wav = "temp.wav"
    audio.export(temp_wav, format="wav")

    # Normalize the waveform data
    max_val = np.max(np.abs(raw_data))
    if max_val > 0:
        raw_data = raw_data / max_val

    return raw_data, temp_wav

def draw_waveform(screen, wave_data, width, height):
    middle_y = height // 2
    scale_x = len(wave_data) / width
    scale_y = middle_y

    for x in range(width):
        index = int(x * scale_x)
        if index < len(wave_data):
            y = int(wave_data[index] * scale_y)
            pygame.draw.line(screen, (0, 255, 0), (x, middle_y - y), (x, middle_y + y))

def main(filename):
    wave_data, wavefile = load_wave_and_raw_data(filename)

    # Initialize Pygame
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Audio Waveform')

    clock = pygame.time.Clock()

    # Load the audio file
    pygame.mixer.init()
    pygame.mixer.music.load(wavefile)

    running = True
    playing = False
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
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

if __name__ == "__main__":
    audio_file = "temp.wav"  # 指定要读取的音频文件
    main(audio_file)
