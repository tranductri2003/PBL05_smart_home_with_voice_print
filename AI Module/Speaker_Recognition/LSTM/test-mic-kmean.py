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
from sklearn.cluster import KMeans
from collections import defaultdict

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

# Hàm để tạo cụm cho mỗi người
def get_clusters(base_embedding_vectors):
    kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=0, n_init=10).fit(base_embedding_vectors)
    return kmeans.cluster_centers_


N_TAKEN_AUDIO = 2 #Best: 10 Should: 2 (Best: 93%, Should: 92%, Each audio: 20s)
K_CLUSTERS = 2# N_TAKEN_AUDIO if N_TAKEN_AUDIO < 5 else 5  #Best: 2 Should 2  (Best: 93%, Should: 92%, Each audio: 20s)

    
# Load pre-trained encoder
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\nhi_model\mfcc_lstm_model_100k_specaug_batch_8_saved_model.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)


tri_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data hôm nay\Trí"
phat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data hôm nay\Phát"
dat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data hôm nay\Đạt"
tuan_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data hôm nay\Tuấn"

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

# Tạo cụm cho mỗi người
tri_clusters = get_clusters(tri_base_embedding_vectors)
phat_clusters = get_clusters(phat_base_embedding_vectors)
dat_clusters = get_clusters(dat_base_embedding_vectors)
tuan_clusters = get_clusters(tuan_base_embedding_vectors)

print("Tri clusters:", len(tri_clusters), len(tri_clusters[0]))
print("Phat clusters:", len(phat_clusters), len(phat_clusters[0]))
print("Dat clusters:", len(dat_clusters), len(dat_clusters[0]))
print("Tuan clusters:", len(tuan_clusters), len(tuan_clusters[0]))

speaker_cluster = defaultdict(lambda: "")
clusters_data = []

for cluster in tri_clusters:
    speaker_cluster[tuple(cluster)] = "Trí"
    clusters_data.append(cluster)
for cluster in phat_clusters:
    speaker_cluster[tuple(cluster)] = "Phát"
    clusters_data.append(cluster)
for cluster in dat_clusters:
    speaker_cluster[tuple(cluster)] = "Đạt"
    clusters_data.append(cluster)
for cluster in tuan_clusters:
    speaker_cluster[tuple(cluster)] = "Tuấn"
    clusters_data.append(cluster)

print(len(clusters_data), len(clusters_data[0]))


# Ghi âm trong 5 giây và lưu vào file "recorded_audio.wav"
record_audio("recorded_audio.wav", duration=10)
current_directory = os.path.dirname(__file__)
audio_file_path = os.path.join(current_directory, "recorded_audio.wav")

audio_file_embedding = inference.get_embedding(audio_file_path, encoder)

# Đọc file âm thanh để lấy thông tin về tần số lấy mẫu
fs, _ = wav.read(audio_file_path)
print(f"Sample rate of recorded_audio.wav: {fs} Hz")

cluster_distance = defaultdict(lambda: 0)
for cluster in clusters_data:
    cluster_distance[tuple(cluster)] = inference.compute_distance(cluster, audio_file_embedding)
    
min_distance = min(cluster_distance.values())
for cluster in clusters_data:
    if inference.compute_distance(cluster, audio_file_embedding) == min_distance:
        prediction = speaker_cluster[tuple(cluster)]
        break

print(prediction)

for cluster in clusters_data:
    cluster_embedding = np.array(cluster)
    cluster_distance = inference.compute_distance(cluster_embedding, audio_file_embedding)
    print(f"Speaker: {speaker_cluster[tuple(cluster)]} Distance to cluster: {cluster_distance}")