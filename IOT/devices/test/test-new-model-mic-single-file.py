import pyaudio
import wave
import time
import os
import signal
from pydub import AudioSegment
from threading import Thread


import os
import torch
import neural_net
import time
import inference
import myconfig
import csv
from pydub import AudioSegment
import tempfile
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



# Thiết lập các tham số ghi âm
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 3  
RAW_FILENAME = "test-new-model-mic/temp_audio_recording_raw.wav"
RESAMPLED_FILENAME = "test-new-model-mic/temp_audio_recording_resampled_raw.wav"

if not os.path.exists("test-new-model-mic"):
    os.makedirs("test-new-model-mic")
    
import RPi.GPIO as GPIO
import time

class TouchSensor:
    def __init__(self, pin):
        self.pin = pin
        # Thiết lập chế độ đánh số chân GPIO
        GPIO.setmode(GPIO.BCM)
        # Đặt chân GPIO làm đầu vào và bật lên điện trở pull-up
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_touched(self):
        # Đọc trạng thái của cảm biến chạm
        return GPIO.input(self.pin) == GPIO.HIGH

    def cleanup(self):
        # Dọn dẹp GPIO
        GPIO.cleanup()



# Khởi tạo PyAudio
audio = pyaudio.PyAudio()
touch_sensor = TouchSensor(22)

frames = []

def signal_handler(sig, frame):
    print("\nRecording stopped.")
    save_and_convert_audio()
    os._exit(0)

def get_unique_filename(filename):
    """Tạo tên tệp duy nhất với thời gian như một phần của tên."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}_{int(time.time())}{ext}"  # Sử dụng thời gian như một phần của tên file
    while os.path.exists(new_filename):
        new_filename = f"{base}_{int(time.time())}_copy{counter}{ext}"
        counter += 1
    return new_filename

def save_and_convert_audio():
    raw_filename = get_unique_filename(RAW_FILENAME)
    resampled_filename = get_unique_filename(RESAMPLED_FILENAME)
    
    # Lưu âm thanh vào file WAV
    with wave.open(raw_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Chuyển đổi tần số lấy mẫu về 16000 Hz
    convert_sample_rate(raw_filename, resampled_filename, 16000)
    print(f"Saved raw audio to {raw_filename}")
    print(f"Saved and resampled audio to {resampled_filename}")
    
    
    users = ["Trí", "Đạt", "Phát"]

    audio_test = AudioSegment.from_wav(resampled_filename)
    extended_audio = extend_audio(audio_test, times=N_TIMES_DUPLICATE)
    audio_file_embedding = get_embedding_from_audiosegment(extended_audio, encoder)
    
    tri_distance = inference.compute_cosine_similarity(tri_base_embedding, audio_file_embedding)
    dat_distance = inference.compute_cosine_similarity(dat_base_embedding, audio_file_embedding)
    # tuan_distance = inference.compute_cosine_similarity(tuan_base_embedding, audio_file_embedding)
    phat_distance = inference.compute_cosine_similarity(phat_base_embedding, audio_file_embedding)
    
    data_distance = [tri_distance, dat_distance, phat_distance]
    print(data_distance)
    prediction = users[data_distance.index(min(data_distance))]
    print(prediction)
    

def convert_sample_rate(input_filename, output_filename, target_sample_rate):
    sound = AudioSegment.from_file(input_filename)
    sound = sound.set_frame_rate(target_sample_rate)
    sound.export(output_filename, format="wav")

def record_audio():
    global frames
    frames.clear()  # Làm trống danh sách frames để bắt đầu ghi âm mới
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    start_time = time.time()
    while touch_sensor.is_touched():  # Ghi âm khi nút bấm được nhấn
        data = stream.read(CHUNK)
        frames.append(data)
        elapsed_time = time.time() - start_time
        print(f"Recording time: {elapsed_time:.2f} seconds", end="\r")
        if elapsed_time > RECORD_SECONDS:
            break

    # Dừng ghi âm
    stream.stop_stream()
    stream.close()
    print("\nFinished recording.")
    save_and_convert_audio()





N_TIMES_DUPLICATE = 1

def extend_audio(audio, times=5):
    return audio * times

def get_embedding_from_audiosegment(audio, encoder):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        audio.export(tmpfile.name, format="wav")
        embedding = inference.get_embedding(tmpfile.name, encoder)
    os.remove(tmpfile.name)
    return embedding


# Load pre-trained encoder
encoder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/saved_model_20240606215142.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)

tri_audio = AudioSegment.from_wav(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/Tri-Merge_Audio.wav")
dat_audio = AudioSegment.from_wav(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/Dat-Merge_Audio.wav")
# # tuan_audio = AudioSegment.from_wav(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/TUAN_5_MINUTES_recording_resampled.wav")
phat_audio = AudioSegment.from_wav(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/Phat-Merge_Audio.wav")

extended_tri_audio = extend_audio(tri_audio, times=N_TIMES_DUPLICATE)
extended_dat_audio = extend_audio(dat_audio, times=N_TIMES_DUPLICATE)
# # extended_tuan_audio = extend_audio(tuan_audio, times=N_TIMES_DUPLICATE)
extended_phat_audio = extend_audio(phat_audio, times=N_TIMES_DUPLICATE)

tri_base_embedding = get_embedding_from_audiosegment(extended_tri_audio, encoder)
print("DONE")
dat_base_embedding = get_embedding_from_audiosegment(extended_dat_audio, encoder)
print("DONE")
# # tuan_base_embedding = get_embedding_from_audiosegment(extended_tuan_audio, encoder)
print("DONE")
phat_base_embedding = get_embedding_from_audiosegment(extended_phat_audio, encoder)
print("DONE")

try:
    while True:
        if touch_sensor.is_touched(): # Nếu nút bấm được nhấn
            record_audio()
except KeyboardInterrupt:
    pass
finally:
    # Dọn dẹp GPIO và PyAudio
    GPIO.cleanup()
    audio.terminate()

    