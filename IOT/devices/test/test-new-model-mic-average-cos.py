# import pyaudio
# import wave
# import time
# import os
# import signal
# from pydub import AudioSegment
# from threading import Thread
# from collections import defaultdict, Counter

# import os
# import torch
# import neural_net
# import time
# import inference
# import myconfig
# import csv
# from pydub import AudioSegment
# import tempfile
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt



# # Thiết lập các tham số ghi âm
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 512
# RECORD_SECONDS = 3  
# RAW_FILENAME = "test-new-model-mic/temp_audio_recording_raw.wav"
# RESAMPLED_FILENAME = "test-new-model-mic/temp_audio_recording_resampled_raw.wav"

# if not os.path.exists("test-new-model-mic"):
#     os.makedirs("test-new-model-mic")
    
# import RPi.GPIO as GPIO
# import time

# class TouchSensor:
#     def __init__(self, pin):
#         self.pin = pin
#         # Thiết lập chế độ đánh số chân GPIO
#         GPIO.setmode(GPIO.BCM)
#         # Đặt chân GPIO làm đầu vào và bật lên điện trở pull-up
#         GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#     def is_touched(self):
#         # Đọc trạng thái của cảm biến chạm
#         return GPIO.input(self.pin) == GPIO.HIGH

#     def cleanup(self):
#         # Dọn dẹp GPIO
#         GPIO.cleanup()



# # Khởi tạo PyAudio
# audio = pyaudio.PyAudio()
# touch_sensor = TouchSensor(22)

# frames = []

# def signal_handler(sig, frame):
#     print("\nRecording stopped.")
#     save_and_convert_audio()
#     os._exit(0)

# def get_unique_filename(filename):
#     """Tạo tên tệp duy nhất với thời gian như một phần của tên."""
#     base, ext = os.path.splitext(filename)
#     counter = 1
#     new_filename = f"{base}_{int(time.time())}{ext}"  # Sử dụng thời gian như một phần của tên file
#     while os.path.exists(new_filename):
#         new_filename = f"{base}_{int(time.time())}_copy{counter}{ext}"
#         counter += 1
#     return new_filename

# def save_and_convert_audio():
#     raw_filename = get_unique_filename(RAW_FILENAME)
#     resampled_filename = get_unique_filename(RESAMPLED_FILENAME)
    
#     # Lưu âm thanh vào file WAV
#     with wave.open(raw_filename, 'wb') as wf:
#         wf.setnchannels(CHANNELS)
#         wf.setsampwidth(audio.get_sample_size(FORMAT))
#         wf.setframerate(RATE)
#         wf.writeframes(b''.join(frames))

#     # Chuyển đổi tần số lấy mẫu về 16000 Hz
#     convert_sample_rate(raw_filename, resampled_filename, 16000)
#     print(f"Saved raw audio to {raw_filename}")
#     print(f"Saved and resampled audio to {resampled_filename}")
    
    
#     audio_test = AudioSegment.from_wav(resampled_filename)
#     extended_audio = extend_audio(audio_test, times=N_TIMES_DUPLICATE)
#     audio_file_embedding = get_embedding_from_audiosegment(extended_audio, encoder)
    
    
#     tri_vector_distances = [inference.compute_cosine_similarity(vector, audio_file_embedding) for vector in tri_base_embedding_vectors]
#     dat_vector_distances = [inference.compute_cosine_similarity(vector, audio_file_embedding) for vector in dat_base_embedding_vectors]
#     # tuan_vector_distances = [inference.compute_cosine_similarity(vector, audio_file_embedding) for vector in tuan_base_embedding_vectors]
#     phat_vector_distances = [inference.compute_cosine_similarity(vector, audio_file_embedding) for vector in phat_base_embedding_vectors]
    
#     tri_vector_distance = np.mean(tri_vector_distances)
#     dat_vector_distance = np.mean(dat_vector_distances)
#     # # tuan_vector_distance = np.mean(tuan_vector_distances)
#     phat_vector_distance = np.mean(phat_vector_distances)
    
#     print(f"tri: {tri_vector_distance}")
#     print(f"dat: {dat_vector_distance}")
#     # # print(f"tuan: {tuan_vector_distance}")
#     print(f"phat: {phat_vector_distance}")
    
#     distances = {
#         "Trí": tri_vector_distance,
#         "Đạt": dat_vector_distance,
#         # "Tuấn": tuan_vector_distance,
#         "Phát": phat_vector_distance
#     }
    
    
#     predicted_speaker = min(distances, key=distances.get)
#     print(f"\033[94mNgười được dự đoán: {predicted_speaker}\033[0m")
    
#     # # Tính khoảng cách giữa file âm thanh và các vector nhúng
#     # embedding_vector_distance = [(vector, inference.compute_cosine_similarity(vector, audio_file_embedding)) for vector in embedding_vectors_data]
    
#     # # Sắp xếp các vector nhúng theo khoảng cách tăng dần
#     # sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])
    
#     # # Dự đoán người nói sử dụng KNN
#     # speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS]]

#     # prediction = Counter(speaker_predictions).most_common(1)[0][0]  

#     # for i in range(K_NEAREST_NEIGHBOURS):
#     #     print(sorted_embedding_vector_distance[i][1])
#     # print(speaker_predictions)
#     # print(prediction)
    

# def convert_sample_rate(input_filename, output_filename, target_sample_rate):
#     sound = AudioSegment.from_file(input_filename)
#     sound = sound.set_frame_rate(target_sample_rate)
#     sound.export(output_filename, format="wav")

# def record_audio():
#     global frames
#     frames.clear()  # Làm trống danh sách frames để bắt đầu ghi âm mới
#     stream = audio.open(format=FORMAT, channels=CHANNELS,
#                         rate=RATE, input=True,
#                         frames_per_buffer=CHUNK)
#     print("Recording...")

#     start_time = time.time()
#     while touch_sensor.is_touched():  # Ghi âm khi nút bấm được nhấn
#         data = stream.read(CHUNK)
#         frames.append(data)
#         elapsed_time = time.time() - start_time
#         print(f"Recording time: {elapsed_time:.2f} seconds", end="\r")
#         if elapsed_time > RECORD_SECONDS:
#             break

#     # Dừng ghi âm
#     stream.stop_stream()
#     stream.close()
#     print("\nFinished recording.")
#     save_and_convert_audio()





# N_TIMES_DUPLICATE = 5
# N_TAKEN_AUDIO = 300 #Best: 10 Should: 2 (Best: 93%, Should: 92%, Each audio: 20s)
# K_NEAREST_NEIGHBOURS = 5# N_TAKEN_AUDIO if N_TAKEN_AUDIO < 5 else 5  #Best: 2 Should 2  (Best: 93%, Should: 92%, Each audio: 20s)


# def extend_audio(audio, times=5):
#     return audio * times

# def get_embedding_from_audiosegment(audio, encoder):
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
#         audio.export(tmpfile.name, format="wav")
#         embedding = inference.get_embedding(tmpfile.name, encoder)
#     os.remove(tmpfile.name)
#     return embedding


# # Load pre-trained encoder
# encoder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/saved_model_20240606215142.pt"
# encoder = neural_net.get_speaker_encoder(encoder_path)

# tri_folder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic/Trí"
# phat_folder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic/Phát"
# dat_folder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic/Đạt"
# # tuan_folder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic/Tuấn"


# tri_audio_files = [file for file in os.listdir(tri_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
# phat_audio_files = [file for file in os.listdir(phat_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
# dat_audio_files = [file for file in os.listdir(dat_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
# # # tuan_audio_files = [file for file in os.listdir(tuan_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]

# tri_base_embedding_vectors = [inference.get_embedding(os.path.join(tri_folder_path, audio), encoder) for audio in tri_audio_files]
# print("Xong Trí")
# phat_base_embedding_vectors = [inference.get_embedding(os.path.join(phat_folder_path, audio), encoder) for audio in phat_audio_files]
# print("Xong Phát")
# dat_base_embedding_vectors = [inference.get_embedding(os.path.join(dat_folder_path, audio), encoder) for audio in dat_audio_files]
# print("Xong Đạt")
# # # # tuan_base_embedding_vectors = [inference.get_embedding(os.path.join(tuan_folder_path, audio), encoder) for audio in tuan_audio_files]
# # print("Xong Tuấn")



# speaker_embedding_vector = defaultdict(lambda: "")
# embedding_vectors_data = []

# for vector in tri_base_embedding_vectors:
#     speaker_embedding_vector[tuple(vector)] = "Trí"
#     embedding_vectors_data.append(vector)
# for vector in phat_base_embedding_vectors:
#     speaker_embedding_vector[tuple(vector)] = "Phát"
#     embedding_vectors_data.append(vector)
# for vector in dat_base_embedding_vectors:
#     speaker_embedding_vector[tuple(vector)] = "Đạt"
#     embedding_vectors_data.append(vector)
# # for vector in tuan_base_embedding_vectors:
#     # speaker_embedding_vector[tuple(vector)] = "Tuấn"
#     # embedding_vectors_data.append(vector)

# print("Ready...")

# try:
#     while True:
#         if touch_sensor.is_touched(): # Nếu nút bấm được nhấn
#             record_audio()
# except KeyboardInterrupt:
#     pass
# finally:
#     # Dọn dẹp GPIO và PyAudio
#     GPIO.cleanup()
#     audio.terminate()

    