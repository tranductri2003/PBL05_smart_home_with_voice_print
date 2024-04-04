import os
import torch
import neural_net
import time
import inference
import myconfig
import csv
from sklearn.cluster import KMeans
from collections import defaultdict

# Hàm để tạo cụm cho mỗi người
def get_clusters(base_embedding_vectors):
    kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=0, n_init=10).fit(base_embedding_vectors)
    return kmeans.cluster_centers_

start_time = time.time()

N_TAKEN_AUDIO = 2 #Best: 10 Should: 2 (Best: 93%, Should: 92%, Each audio: 20s)
K_CLUSTERS = 2# N_TAKEN_AUDIO if N_TAKEN_AUDIO < 5 else 5  #Best: 2 Should 2  (Best: 93%, Should: 92%, Each audio: 20s)

# Load pre-trained encoder
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)


tri_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói base\Trí"
phat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói base\Phát"
dat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói base\Đạt"
tuan_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói base\Tuấn"

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


DATA_SOURCE = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói tổng hợp"

total_prediction = 0 
accurate_prediction = 0

for user in os.listdir(DATA_SOURCE):
    user_folder_path = os.path.join(DATA_SOURCE, user)
    for audio_file in os.listdir(user_folder_path):
        audio_file_path = os.path.join(user_folder_path, audio_file)
        
        audio_file_embedding = inference.get_embedding(audio_file_path, encoder)
        
        cluster_distance = defaultdict(lambda: 0)
        for cluster in clusters_data:
            cluster_distance[tuple(cluster)] = inference.compute_distance(cluster, audio_file_embedding)
            
        min_distance = min(cluster_distance.values())
        for cluster in clusters_data:
            if inference.compute_distance(cluster, audio_file_embedding) == min_distance:
                prediction = speaker_cluster[tuple(cluster)]
                break

        if user == prediction:
            print(f"\033[94mSpeaker: {user} Predict: {prediction} [TRUE]\033[0m")
            accurate_prediction += 1
        else:
            print(f"\033[91mSpeaker: {user} Predict: {prediction} [FALSE]\033[0m")
        
        total_prediction += 1



end_time = time.time()
print(end_time - start_time)

print(f"Model: {encoder_path}")
print(f"Seq length: {myconfig.SEQ_LEN}")
print(f"Accurate prediction: {accurate_prediction}")
print(f"Total prediction: {total_prediction}")
print(f"Accuracy: {accurate_prediction / total_prediction*100}%  ")



