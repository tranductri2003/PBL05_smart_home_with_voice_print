import os
import torch
import neural_net
import inference
import myconfig
from collections import defaultdict
import csv

MODEL_PATHS = [
    # r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\nhi's model\mfcc_2lstm_model_100k_specaug_batch_8_saved_model.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\nhi's model\mfcc_lstm_model_100k_specaug_batch_8_saved_model.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-100-hours-100-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_100h_100epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-100-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_100epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-20000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_20000epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-gpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_gpu.pt",
    # r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-4-stacks-cpu\mfcc_lstm_model_360h_50000epochs_specaug_8batch_4stacks_cpu.pt",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-other-500-hours-50000-epochs-specaug-8-batch-3-stacks-cpu\mfcc_lstm_model_500h_10000epochs_specaug_8batch_3stacks_cpu.pt",
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
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói tổng hợp",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói để train",
    r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói để điều khiển nhà"
]

DATASET_NAMES = [
    "Data Tiếng nói tổng hợp",
    "Data Tiếng nói để train",
    "Data Tiếng nói để điều khiển nhà",
]

DATASET_BASE_PATH = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói base"

SPEAKERS = [
    "Trí",
    "Đạt",
    "Tuấn",
    "Phát"
]

csv_file_path = "statistic-test-models-single-audio-file.csv"

data = [("Model", "Test Dataset", "EER-Threshold", "Accurate Prediction", "Total Prediction", "Percentage")]

for i, model_path in enumerate(MODEL_PATHS):
    # Load pre-trained encoder
    encoder = neural_net.get_speaker_encoder(model_path)

    embedding_vector = defaultdict(list)
    for speaker in SPEAKERS:
        speaker_folder_path = os.path.join(DATASET_BASE_PATH, speaker)
        if os.path.exists(speaker_folder_path):
            audio_files = [f for f in os.listdir(speaker_folder_path) if f.endswith('.wav')]
            if audio_files:
                audio_file_path = os.path.join(speaker_folder_path, audio_files[0])
                embedding_vector[speaker] = inference.get_embedding(audio_file_path, encoder)
            else:
                print(f"No audio files found in folder {speaker_folder_path}")
        else:
            print(f"Folder {speaker_folder_path} does not exist")
    
    
    for j, dataset_test_path in enumerate(DATASET_TEST_PATH):
        total_prediction = 0 
        accurate_prediction = 0

        for speaker in os.listdir(dataset_test_path):
            speaker_folder_path = os.path.join(dataset_test_path, speaker)
            for audio_file in os.listdir(speaker_folder_path):
                audio_file_path = os.path.join(speaker_folder_path, audio_file)
                audio_file_embedding = inference.get_embedding(audio_file_path, encoder)
                
                speaker_distance = defaultdict(lambda:0)
                for user in SPEAKERS:
                    speaker_distance[user] = inference.compute_distance(embedding_vector[user], audio_file_embedding)

                for user in SPEAKERS:
                    if speaker_distance[user] == min(speaker_distance.values()):
                        prediction = user
                        break

                accurate_prediction += 1 if prediction == speaker else 0
                total_prediction += 1

        data.append((MODEL_NAMES[i], DATASET_NAMES[j], 0, accurate_prediction, total_prediction, accurate_prediction/total_prediction*100))
        
        print(f"Model: {MODEL_NAMES[i]}")
        # print(f"Seq length: {myconfig.SEQ_LEN}")
        print(f"Accurate prediction: {accurate_prediction}")
        print(f"Total prediction: {total_prediction}")
        print(f"Accuracy: {accurate_prediction / total_prediction*100}%  ")


# Ghi dữ liệu vào file CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV file 'statistic-train-models-single-audio-file.csv' has been created successfully.")