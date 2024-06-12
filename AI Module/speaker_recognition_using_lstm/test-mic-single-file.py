import os
import torch
import neural_net
import time
import inference
import myconfig
import csv
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import resample
import subprocess
import tensorflow as tf


def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', input_path, '-ar', str(target_sample_rate), output_path]
    subprocess.run(command, check=True)
    
    
def record_audio(file_name, duration, sample_rate=44100, target_sample_rate=16000):
    # Lấy đường dẫn thư mục hiện hành của file mã nguồn
    current_directory = os.path.dirname(__file__)
    # Kết hợp đường dẫn của thư mục hiện hành với tên file để tạo đường dẫn đầy đủ
    file_path = os.path.join(current_directory, file_name)

    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    print("Recording finished.")

    # Lưu file âm thanh vào thư mục hiện hành với tần số lấy mẫu mới
    wav.write(file_path, sample_rate, audio_data)
    
    # Lưu tạm thời tệp đã chuyển đổi
    temp_path = file_path + '.temp.wav'
    convert_sample_rate(file_path, temp_path, target_sample_rate)
    # Thay thế tệp gốc bằng tệp đã chuyển đổi
    os.replace(temp_path, file_path)
    print(f"Audio saved as {file_path} with sample rate {target_sample_rate} Hz")


    

# Load pre-trained encoder
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\nhi_model\mfcc_lstm_model_100k_specaug_batch_8_saved_model.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)


tri_base_embedding = inference.get_embedding(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Trí\tri_resampled.wav", encoder)
dat_base_embedding = inference.get_embedding(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Đạt\dat_resampled.wav", encoder)
tuan_base_embedding = inference.get_embedding(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Tuấn\tuan_resampled.wav", encoder)
phat_base_embedding = inference.get_embedding(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Phát\phat_resampled.wav", encoder)


# Ghi âm trong 5 giây và lưu vào file "recorded_audio.wav"
record_audio("recorded_audio.wav", duration=10)
current_directory = os.path.dirname(__file__)
audio_file_path = os.path.join(current_directory, "recorded_audio.wav")

audio_file_embedding = inference.get_embedding(audio_file_path, encoder)

# Đọc file âm thanh để lấy thông tin về tần số lấy mẫu
fs, _ = wav.read(audio_file_path)
print(f"Sample rate of recorded_audio.wav: {fs} Hz")



tri_distance = inference.compute_distance(tri_base_embedding, audio_file_embedding)
dat_distance = inference.compute_distance(dat_base_embedding, audio_file_embedding)
tuan_distance = inference.compute_distance(tuan_base_embedding, audio_file_embedding)
phat_distance = inference.compute_distance(phat_base_embedding, audio_file_embedding)

print(f"Tri distance: {tri_distance}")
print(f"Dat distance: {dat_distance}")
print(f"Tuan distance: {tuan_distance}")
print(f"Phat distance: {phat_distance}")

data_distance = []
data_distance.append(tri_distance)
data_distance.append(dat_distance)
data_distance.append(tuan_distance)
data_distance.append(phat_distance)

users = ["Trí", "Đạt", "Tuấn", "Phát"]
prediction = users[data_distance.index(min(data_distance))]
print(prediction)