import os
import torch
import neural_net
import time
import inference
import myconfig
import csv
from collections import defaultdict, Counter

start_time = time.time()

N_TAKEN_AUDIO = 5 #Best: 10 Should: 2 (Best: 93%, Should: 92%, Each audio: 20s)
K_NEAREST_NEIGHBOURS = 3# N_TAKEN_AUDIO if N_TAKEN_AUDIO < 5 else 5  #Best: 2 Should 2  (Best: 93%, Should: 92%, Each audio: 20s)

# Load pre-trained encoder
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\nhi_model\models_transformer_mfcc_200k_specaug_batch_8.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)


tri_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Trí"
phat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Phát"
dat_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Đạt"
tuan_folder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Tuấn"

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


    
    
DATA_SOURCE = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói tổng hợp"

total_prediction = 0 
accurate_prediction = 0

# audio_file_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\recorded_audio.wav"

# # Nhúng file âm thanh
# audio_file_embedding = inference.get_embedding(audio_file_path, encoder)

# # Tính khoảng cách giữa file âm thanh và các vector nhúng
# embedding_vector_distance = [(vector, inference.compute_distance(vector, audio_file_embedding)) for vector in embedding_vectors_data]

# # Sắp xếp các vector nhúng theo khoảng cách tăng dần
# sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])

# # Dự đoán người nói sử dụng KNN
# speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS]]

# prediction = Counter(speaker_predictions).most_common(1)[0][0]        

# print(prediction)
# total_prediction += 1




for speaker in os.listdir(DATA_SOURCE):
    speaker_folder_path = os.path.join(DATA_SOURCE, speaker)
    # Duyệt qua từng file âm thanh của người này
    for audio_file in os.listdir(speaker_folder_path):
        audio_file_path = os.path.join(speaker_folder_path, audio_file)
        
        # Nhúng file âm thanh
        audio_file_embedding = inference.get_embedding(audio_file_path, encoder)
        
        # Tính khoảng cách giữa file âm thanh và các vector nhúng
        embedding_vector_distance = [(vector, inference.compute_distance(vector, audio_file_embedding)) for vector in embedding_vectors_data]
        
        # Sắp xếp các vector nhúng theo khoảng cách tăng dần
        sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])
        
        # Dự đoán người nói sử dụng KNN
        speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS]]

        prediction = Counter(speaker_predictions).most_common(1)[0][0]        

        if speaker == prediction:
            print(f"\033[94mSpeaker: {speaker} Predict: {prediction} [TRUE]\033[0m")
            accurate_prediction += 1
        else:
            print(f"\033[91mSpeaker: {speaker} Predict: {prediction} [FALSE]\033[0m")
        
        total_prediction += 1



end_time = time.time()
print(end_time - start_time)

print(f"Model: {encoder_path}")
print(f"Seq length: {myconfig.SEQ_LEN}")
print(f"Accurate prediction: {accurate_prediction}")
print(f"Total prediction: {total_prediction}")
print(f"Accuracy: {accurate_prediction / total_prediction*100}%  ")



