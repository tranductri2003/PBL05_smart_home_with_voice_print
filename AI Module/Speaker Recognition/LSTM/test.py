import os
import torch
import neural_net
import time
import inference
import myconfig




# Load pre-trained encoder
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\saved_model\train-clean-360-hours-50000-epochs\saved_model_20240320203146.ckpt-20000.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)

start_time = time.time()

tri_base_embedding = inference.get_embedding(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói tổng hợp\Trí\tri_1.wav", encoder)
dat_base_embedding = inference.get_embedding(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói tổng hợp\Đạt\DAT_1.wav", encoder)
tuan_base_embedding = inference.get_embedding(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói tổng hợp\Tuấn\tuan_0.wav", encoder)
phat_base_embedding = inference.get_embedding(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói tổng hợp\Phát\phat_1.wav", encoder)



data_source = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker Recognition\LSTM\Data Tiếng nói để train"

total_prediction = 0 
accurate_prediction = 0

for user in os.listdir(data_source):
    user_folder_path = os.path.join(data_source, user)
    for audio_file in os.listdir(user_folder_path):
        audio_file_path = os.path.join(user_folder_path, audio_file)
        
        audio_file_embedding = inference.get_embedding(audio_file_path, encoder)
        
        tri_distance = inference.compute_distance(tri_base_embedding, audio_file_embedding)
        dat_distance = inference.compute_distance(dat_base_embedding, audio_file_embedding)
        tuan_distance = inference.compute_distance(tuan_base_embedding, audio_file_embedding)
        phat_distance = inference.compute_distance(phat_base_embedding, audio_file_embedding)
        
        data_distance = []
        data_distance.append(tri_distance)
        data_distance.append(dat_distance)
        data_distance.append(tuan_distance)
        data_distance.append(phat_distance)

        users = ["Trí", "Đạt", "Tuấn", "Phát"]
        prediction = users[data_distance.index(min(data_distance))]

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



