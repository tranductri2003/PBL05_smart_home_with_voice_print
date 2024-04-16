import os
import torch
import neural_net
import time
import inference
import myconfig
import csv
from collections import defaultdict, Counter



start_time = time.time()

N_TAKEN_AUDIO = [5, 7, 10]
K_NEAREST_NEIGHBOURS = [3, 5, 7]   #math.sqrt(len(dataset))

MODEL_PATHS = [
    # r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\nhi's model\mfcc_2lstm_model_100k_specaug_batch_8_saved_model.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\nhi's model\mfcc_lstm_model_100k_specaug_batch_8_saved_model.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\train-clean-100-hours-100-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_100h_100epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\train-clean-360-hours-100-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_100epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\train-clean-360-hours-20000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_20000epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-gpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_gpu.pt",
    # r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-4-stacks-cpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_4stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\saved_model\train-other-500-hours-50000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_500h_10000epochs_specaug_8batch_3stacks_cpu.pt",
]

MODEL_NAMES = [
    # "mfcc_2lstm_model_100k_specaug_batch_8_saved_model.pt",
    "mfcc_lstm_model_100k_specaug_batch_8_saved_model.pt",
    "mfcc_lstm_model_100h_100epochs_specaug_8batch_3stacks_cpu.pt",
    "mfcc_lstm_model_360h_100epochs_specaug_8batch_3stacks_cpu.pt",
    "mfcc_lstm_model_360h_20000epochs_specaug_8batch_3stacks_cpu.pt",
    "mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt",
    "mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_gpu.pt",
    #"mfcc_lstm_model_360h_50000epochs_specaug_8batch_4stacks_cpu.pt",
    "mfcc_lstm_model_500h_10000epochs_specaug_8batch_3stacks_cpu.pt",
]

DATASET_TEST_PATH = [
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói tổng hợp",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói để train",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói để điều khiển nhà"
]

DATASET_NAMES = [
    "Data Tiếng nói tổng hợp",
    "Data Tiếng nói để train",
    "Data Tiếng nói để điều khiển nhà",
]

DATASET_BASE_PATH = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base"

SPEAKERS = [
    "Trí",
    "Đạt",
    "Tuấn",
    "Phát"
]

csv_file_path = "statistic-test-models-knn.csv"

data = [("Model", "Test Dataset", "EER-Threshold", "N_Taken Audio", "K-Nearest Neighbours", "Accurate Prediction", "Total Prediction", "Percentage")]

speaker_folder_path = defaultdict(lambda:"")
for speaker in SPEAKERS:
    speaker_folder_path[speaker] = os.path.join(DATASET_BASE_PATH, speaker)

speaker_audio_files = defaultdict(list)
for speaker in SPEAKERS:
    speaker_audio_files[speaker] = [file for file in os.listdir(speaker_folder_path[speaker])]
    
for i, model_path in enumerate(MODEL_PATHS):
    # Load pre-trained encoder
    encoder = neural_net.get_speaker_encoder(model_path)
    
    speaker_base_embedding_vectors = defaultdict(list)
    for speaker in SPEAKERS:
        speaker_base_embedding_vectors[speaker] = [inference.get_embedding(os.path.join(speaker_folder_path[speaker], audio), encoder) for audio in speaker_audio_files[speaker]]
    
    for j, n_taken_audio in enumerate(N_TAKEN_AUDIO):
        speaker_base_embedding_vectors_n_taken = defaultdict(list)
        for speaker in SPEAKERS:
            speaker_base_embedding_vectors_n_taken[speaker] = speaker_base_embedding_vectors[speaker][:n_taken_audio]
            
        speaker_embedding_vector = defaultdict(lambda: "")
        embedding_vectors_data = []
        
        for speaker in SPEAKERS:
            for vector in speaker_base_embedding_vectors_n_taken[speaker]:
                speaker_embedding_vector[tuple(vector)] = speaker
                embedding_vectors_data.append(vector)
        
        for k, dataset_test_path in enumerate(DATASET_TEST_PATH):
            total_prediction = 0
            accurate_prediction = 0

            for user in os.listdir(dataset_test_path):
                user_folder_path = os.path.join(dataset_test_path, user)
                
                for audio_file in os.listdir(user_folder_path):
                    audio_file_path = os.path.join(user_folder_path, audio_file)
                    audio_file_embedding = inference.get_embedding(audio_file_path, encoder)
                    
                    embedding_vector_distance = [(vector, inference.compute_distance(vector, audio_file_embedding)) for vector in embedding_vectors_data]
                    sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])
                    speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS[j]]]

                    prediction = Counter(speaker_predictions).most_common(1)[0][0]        

                    # if user == prediction:
                    #     print(f"\033[94mSpeaker: {user} Predict: {prediction} [TRUE]\033[0m")
                    #     # accurate_prediction += 1
                    # else:
                    #     print(f"\033[91mSpeaker: {user} Predict: {prediction} [FALSE]\033[0m")
                    accurate_prediction += 1 if prediction == user else 0
                    total_prediction += 1


            data.append((MODEL_NAMES[i], DATASET_NAMES[k], 0, n_taken_audio, K_NEAREST_NEIGHBOURS[j], accurate_prediction, total_prediction, accurate_prediction/total_prediction*100))
            
            print(f"Model: {MODEL_NAMES[i]}")
            print(f"Test Dataset: {DATASET_NAMES[k]}")
            print(f"Number of taken audios: {n_taken_audio}")
            print(f"Number of k-nearest neighbours: {K_NEAREST_NEIGHBOURS[j]}")
            print(f"Accurate prediction: {accurate_prediction}")
            print(f"Total prediction: {total_prediction}")
            print(f"Accuracy: {accurate_prediction / total_prediction*100}%  ")
            
# Ghi dữ liệu vào file CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV file 'statistic-test-models-knn.csv' has been created successfully.")