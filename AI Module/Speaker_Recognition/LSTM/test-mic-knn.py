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
from collections import defaultdict, Counter
from pydub import AudioSegment

N_TAKEN_AUDIO = 5 #Best: 10 Should: 2 (Best: 93%, Should: 92%, Each audio: 20s)
K_NEAREST_NEIGHBOURS = 5# N_TAKEN_AUDIO if N_TAKEN_AUDIO < 5 else 5  #Best: 2 Should 2  (Best: 93%, Should: 92%, Each audio: 20s)


def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_frame_rate(target_sample_rate)
    sound.export(output_path, format="wav")
    
def record_audio(file_name, duration, sample_rate=44100, target_sample_rate=16000):
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, file_name)

    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)  # channels=1 để ghi âm kênh mono
    sd.wait()
    print("Recording finished.")

    # Lưu file âm thanh vào thư mục hiện hành với tần số lấy mẫu mới
    wav.write(file_path, sample_rate, audio_data)

    # Chuyển đổi sang kênh mono nếu cần
    if audio_data.shape[1] > 1:  # Kiểm tra xem âm thanh có nhiều hơn một kênh không
        mono_audio_data = np.mean(audio_data, axis=1, dtype=np.int16)  # Lấy trung bình của tất cả các kênh
        wav.write(file_path, sample_rate, mono_audio_data)

    # Lưu tạm thời tệp đã chuyển đổi
    temp_path = file_path + '.temp.wav'
    convert_sample_rate(file_path, temp_path, target_sample_rate)
    # Thay thế tệp gốc bằng tệp đã chuyển đổi
    os.replace(temp_path, file_path)
    print(f"Audio saved as {file_path} with sample rate {target_sample_rate} Hz")



# Load pre-trained encoder
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\nhi_model\mfcc_lstm_model_100k_specaug_batch_8_saved_model.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)


tri_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\BackEnd\audio_resampled_data\Trần Đức Trí"
phat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\BackEnd\audio_resampled_data\Phạm Nguyễn Anh Phát"
dat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\BackEnd\audio_resampled_data\Lê Văn Tiến Đạt"
tuan_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\BackEnd\audio_resampled_data\Lê Anh Tuấn"

# tri_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data hôm nay\Trí"
# phat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data hôm nay\Phát"
# dat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data hôm nay\Đạt"
# tuan_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data hôm nay\Tuấn"


tri_audio_files = [file for file in os.listdir(tri_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
phat_audio_files = [file for file in os.listdir(phat_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
dat_audio_files = [file for file in os.listdir(dat_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
tuan_audio_files = [file for file in os.listdir(tuan_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]

tri_base_embedding_vectors = [inference.get_embedding(os.path.join(tri_folder_path, audio), encoder) for audio in tri_audio_files]
phat_base_embedding_vectors = [inference.get_embedding(os.path.join(phat_folder_path, audio), encoder) for audio in phat_audio_files]
dat_base_embedding_vectors = [inference.get_embedding(os.path.join(dat_folder_path, audio), encoder) for audio in dat_audio_files]
tuan_base_embedding_vectors = [inference.get_embedding(os.path.join(tuan_folder_path, audio), encoder) for audio in tuan_audio_files]

print(len(tri_base_embedding_vectors), len(tri_base_embedding_vectors[0]))
print(len(phat_base_embedding_vectors), len(phat_base_embedding_vectors[0]))
print(len(dat_base_embedding_vectors), len(dat_base_embedding_vectors[0]))
print(len(tuan_base_embedding_vectors), len(tuan_base_embedding_vectors[0]))


speaker_embedding_vector = defaultdict(lambda: "")
embedding_vectors_data = []

for vector in tri_base_embedding_vectors:
    speaker_embedding_vector[tuple(vector)] = "Trí"
    embedding_vectors_data.append(vector)
for vector in phat_base_embedding_vectors:
    speaker_embedding_vector[tuple(vector)] = "Phát"
    embedding_vectors_data.append(vector)
for vector in dat_base_embedding_vectors:
    speaker_embedding_vector[tuple(vector)] = "Đạt"
    embedding_vectors_data.append(vector)
for vector in tuan_base_embedding_vectors:
    speaker_embedding_vector[tuple(vector)] = "Tuấn"
    embedding_vectors_data.append(vector)


# Ghi âm trong 5 giây và lưu vào file "recorded_audio.wav"
record_audio("recorded_audio.wav", duration=3, sample_rate=44100, target_sample_rate=16000)
current_directory = os.path.dirname(__file__)
audio_file_path = os.path.join(current_directory, "recorded_audio.wav")

sounds = [AudioSegment.from_file(audio_file_path, format="wav") for _ in range(20)]
combined = sum(sounds)

file_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM"
file_handle = combined.export(os.path.join(file_path, "audio-combined.wav"), format="wav")
audio_file_path = os.path.join(current_directory, "audio-combined.wav")



# Đọc file âm thanh để lấy thông tin về tần số lấy mẫu
fs, _ = wav.read(audio_file_path)
print(f"Sample rate of recorded_audio.wav: {fs} Hz")

# Nhúng file âm thanh
audio_file_embedding = inference.get_embedding(audio_file_path, encoder)

# Tính khoảng cách giữa file âm thanh và các vector nhúng
embedding_vector_distance = [(vector, inference.compute_distance(vector, audio_file_embedding)) for vector in embedding_vectors_data]

# Sắp xếp các vector nhúng theo khoảng cách tăng dần
sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])

# Dự đoán người nói sử dụng KNN
speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS]]

prediction = Counter(speaker_predictions).most_common(1)[0][0]        

print(speaker_predictions)
print(prediction)