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

N_TIMES_DUPLICATE = 5

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

start_time = time.time()

# Load and extend base audio files
tri_audio = AudioSegment.from_wav(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/TRI_5_MINUTES_recording_resampled.wav")
dat_audio = AudioSegment.from_wav(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/DAT_5_MINUTES_recording_resampled.wav")
tuan_audio = AudioSegment.from_wav(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/TUAN_5_MINUTES_recording_resampled.wav")
phat_audio = AudioSegment.from_wav(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/PHAT_5_MINUTES_recording_resampled.wav")

extended_tri_audio = extend_audio(tri_audio, times=N_TIMES_DUPLICATE)
extended_dat_audio = extend_audio(dat_audio, times=N_TIMES_DUPLICATE)
extended_tuan_audio = extend_audio(tuan_audio, times=N_TIMES_DUPLICATE)
extended_phat_audio = extend_audio(phat_audio, times=N_TIMES_DUPLICATE)

tri_base_embedding = get_embedding_from_audiosegment(extended_tri_audio, encoder)
dat_base_embedding = get_embedding_from_audiosegment(extended_dat_audio, encoder)
tuan_base_embedding = get_embedding_from_audiosegment(extended_tuan_audio, encoder)
phat_base_embedding = get_embedding_from_audiosegment(extended_phat_audio, encoder)

data_source = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic"

total_prediction = 0 
accurate_prediction = 0
users = ["Trí", "Đạt", "Tuấn", "Phát"]
user_index = {user: i for i, user in enumerate(users)}
confusion_matrix = np.zeros((len(users), len(users)), dtype=int)

for user in os.listdir(data_source):
    user_folder_path = os.path.join(data_source, user)
    for audio_file in os.listdir(user_folder_path):
        audio_file_path = os.path.join(user_folder_path, audio_file)
        audio = AudioSegment.from_wav(audio_file_path)
        extended_audio = extend_audio(audio, times=N_TIMES_DUPLICATE)
        audio_file_embedding = get_embedding_from_audiosegment(extended_audio, encoder)
        
        tri_distance = inference.compute_distance(tri_base_embedding, audio_file_embedding)
        dat_distance = inference.compute_distance(dat_base_embedding, audio_file_embedding)
        tuan_distance = inference.compute_distance(tuan_base_embedding, audio_file_embedding)
        phat_distance = inference.compute_distance(phat_base_embedding, audio_file_embedding)
        
        data_distance = [tri_distance, dat_distance, tuan_distance, phat_distance]

        prediction = users[data_distance.index(min(data_distance))]
        
        if user == prediction:
            print(f"\033[94mSpeaker: {user} Predict: {prediction} [TRUE]\033[0m")
            accurate_prediction += 1
        else:
            print(f"\033[91mSpeaker: {user} Predict: {prediction} [FALSE]\033[0m")
        
        confusion_matrix[user_index[user], user_index[prediction]] += 1
        total_prediction += 1

end_time = time.time()

print("Confusion Matrix:")
print(confusion_matrix)

print(f"Model: {encoder_path}")
print(f"Seq length: {myconfig.SEQ_LEN}")
print(f"Accurate prediction: {accurate_prediction}")
print(f"Total prediction: {total_prediction}")
print(f"Accuracy: {accurate_prediction / total_prediction * 100}%")

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.set(font_scale=1.2)
sns.heatmap(confusion_matrix, annot=True, cmap="Blues", fmt="d", xticklabels=users, yticklabels=users)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

"""
import os
import torch
import neural_net
import time
import inference
import myconfig
import csv
from pydub import AudioSegment

def extend_audio(audio, times=5):
    return audio * times

# Load pre-trained encoder
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\saved_model_20240606215142.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)

start_time = time.time()

# Load and extend base audio files
tri_audio = AudioSegment.from_wav(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\Trí-200-5.wav\Tri_base_200s.wav")
dat_audio = AudioSegment.from_wav(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\Đạt-200-5.wav\Dat_base_200s.wav")
tuan_audio = AudioSegment.from_wav(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\Tuấn-200-5.wav\Tuan_base_200s.wav")
phat_audio = AudioSegment.from_wav(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\Phát-200-5.wav\Phat_base_200s.wav")

tri_base_embedding = inference.get_embedding(tri_audio, encoder)
dat_base_embedding = inference.get_embedding(dat_audio, encoder)
tuan_base_embedding = inference.get_embedding(tuan_audio, encoder)
phat_base_embedding = inference.get_embedding(phat_audio, encoder)

data_source = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-dir"

total_prediction = 0 
accurate_prediction = 0

for user in os.listdir(data_source):
    user_folder_path = os.path.join(data_source, user)
    for audio_file in os.listdir(user_folder_path):
        audio_file_path = os.path.join(user_folder_path, audio_file)
        audio = AudioSegment.from_wav(audio_file_path)
        extended_audio = extend_audio(audio, times=5)
        audio_file_embedding = inference.get_embedding(extended_audio, encoder)
        
        tri_distance = inference.compute_distance(tri_base_embedding, audio_file_embedding)
        dat_distance = inference.compute_distance(dat_base_embedding, audio_file_embedding)
        tuan_distance = inference.compute_distance(tuan_base_embedding, audio_file_embedding)
        phat_distance = inference.compute_distance(phat_base_embedding, audio_file_embedding)
        
        data_distance = [tri_distance, dat_distance, tuan_distance, phat_distance]

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
print(f"Accuracy: {accurate_prediction / total_prediction * 200}%")
"""