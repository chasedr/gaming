# # Synchronous audio example using SDL's low-level API.
# import time

# import soundfile  # pip install soundfile
# import tcod.sdl.audio

# device = tcod.sdl.audio.open()  # Open the default output device.
# sound, sample_rate = soundfile.read("button01b.mp3", dtype="float32")  # Load an audio sample using SoundFile.
# converted = device.convert(sound, sample_rate)  # Convert this sample to the format expected by the device.
# device.queue_audio(converted)  # Play audio synchronously by appending it to the device buffer.
# sound, sample_rate = soundfile.read("cow1.mp3", dtype="float32")  # Load an audio sample using SoundFile.
# converted = device.convert(sound, sample_rate)  # Convert this sample to the format expected by the device.
# device.queue_audio(converted)  # Play audio synchronously by appending it to the device buffer.
# sound, sample_rate = soundfile.read("sparrows.mp3", dtype="float32")  # Load an audio sample using SoundFile.
# converted = device.convert(sound, sample_rate)  # Convert this sample to the format expected by the device.
# device.queue_audio(converted)  # Play audio synchronously by appending it to the device buffer.
# sound, sample_rate = soundfile.read("mallard1.mp3", dtype="float32")  # Load an audio sample using SoundFile.
# converted = device.convert(sound, sample_rate)  # Convert this sample to the format expected by the device.
# device.queue_audio(converted)  # Play audio synchronously by appending it to the device buffer.

# while device.queued_samples:  # Wait until device is done playing.
#     time.sleep(0.001)



# used to play voice 
# Asynchronous audio example using BasicMixer.
import time

import soundfile  # pip install soundfile
import tcod.sdl.audio

mixer = tcod.sdl.audio.BasicMixer(tcod.sdl.audio.open())  # Setup BasicMixer with the default audio output.
sound, sample_rate = soundfile.read("cow1.mp3")  # Load an audio sample using SoundFile.
sound = mixer.device.convert(sound, sample_rate)  # Convert this sample to the format expected by the device.
channel = mixer.play(sound, volume=0.05)  # Start asynchronous playback, audio is mixed on a separate Python thread.
sound, sample_rate = soundfile.read("mallard1.mp3")  # Load an audio sample using SoundFile.
sound = mixer.device.convert(sound, sample_rate)  # Convert this sample to the format expected by the device.
channel2 = mixer.play(sound)



while channel.busy:  # Wait until the sample is done playing.
    time.sleep(0.001)
    
    





#used to record voice
import pyaudio
import numpy as np

# 音频参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 打开音频流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* 开始录音")

try:
    while True:
        # 读取音频数据
        data = stream.read(CHUNK)
        # 将字节数据转换为 numpy 数组
        audio_data = np.frombuffer(data, dtype=np.int16)
        # 计算幅度
        amplitude = np.abs(audio_data).max()
        print(f"当前幅度: {amplitude}")

except KeyboardInterrupt:
    print("* 停止录音")

# 停止音频流
stream.stop_stream()
stream.close()
p.terminate()