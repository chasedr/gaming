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