from pydub import AudioSegment

audio_path = 'temp.wav'  # 替换为你的音频路径
converted_audio_path = 'temp_converted.wav'

audio = AudioSegment.from_file(audio_path)
audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
audio.export(converted_audio_path, format='wav')

print(f'Converted audio saved to {converted_audio_path}')
