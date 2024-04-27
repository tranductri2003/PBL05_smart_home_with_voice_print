import os
from collections import defaultdict, Counter
import neural_net
import inference
import myconfig
import dataset
import feature_extraction
import specaug
import time
import pyaudio
import wave
import RPi.GPIO as GPIO
import librosa
import soundfile as sf
import subprocess
from pydub import AudioSegment
import torch
from transformers import pipeline
import speech_recognition as sr


from db_helper import Member, Appliance, Permission, query_members, query_appliances, query_permissions, query_member_files, get_features, connect_db
from utils import convert_sample_rate, speech2text, extract_action_and_device

from Electronic_Devices.servo import ServoController
from Electronic_Devices.motor import MotorController

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SPEECH_RECOGNITION_MODEl = pipeline('automatic-speech-recognition', model='vinai/PhoWhisper-base', device=DEVICE)
    
SPEAKER_RECOGNITION_MODEL_PATH = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/IOT/saved_model/train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-cpu/mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt"   
SPEAKER_RECOGNITION_MODEL = neural_net.get_speaker_encoder(SPEAKER_RECOGNITION_MODEL_PATH)

DB_PATH = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/BackEnd/db.sqlite3"
CONN = connect_db(DB_PATH)

N_TAKEN_AUDIO = 5
K_NEAREST_NEIGHBOURS = 5

# Thiết lập các tham số ghi âm
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512 
RAW_RECORDING_PATH = "/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/BackEnd/audio_raw_data"
RESAMPLED_RATE = 16000  # Tần số lấy mẫu mới

WAVE_OUTPUT_RAW_FILENAME = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/IOT/temp_recorded_audio/recording_raw.wav"
WAVE_OUTPUT_RESAMPLED_FILENAME = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/IOT/temp_recorded_audio/recording_resampled.wav"

# Khởi tạo đối tượng Recognizer
recognizer = sr.Recognizer()

# Khởi tạo PyAudio
audio = pyaudio.PyAudio()

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 26 là chân được kết nối với nút bấm


# Khai báo chân GPIO cho servo
def record_audio():
    # Bắt đầu ghi âm
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    while GPIO.input(26) == GPIO.LOW: # Ghi âm khi nút bấm được nhấn
        data = stream.read(CHUNK)
        frames.append(data)

    # Dừng ghi âm
    stream.stop_stream()
    stream.close()
    
    print("Finished recording.")
    
    # Lưu âm thanh vào file WAV
    with wave.open(WAVE_OUTPUT_RAW_FILENAME, 'wb') as wf:
    
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    
    convert_sample_rate(WAVE_OUTPUT_RAW_FILENAME, WAVE_OUTPUT_RESAMPLED_FILENAME, 16000)

    
    sound = AudioSegment.from_file(WAVE_OUTPUT_RESAMPLED_FILENAME, format="wav")
    duplicated_sound = sound * 30
    duplicated_sound.export(WAVE_OUTPUT_RESAMPLED_FILENAME, format="wav")    
    
    
    members = query_members(CONN)
    permissions = query_permissions(CONN)
    check_permission = defaultdict(lambda: defaultdict(lambda: False))
    for permission in permissions:
        check_permission[permission.member_name][permission.appliance_name] = True
    

        

        
    speaker_base_embedding_vectors = defaultdict(list)
    for member in members:
        speaker_base_embedding_vectors[member.name] = [get_features(vector['features']) for vector in query_member_files(CONN, member.name)]
                
    speaker_embedding_vector = defaultdict(lambda: "")
    embedding_vectors_data = []
    
    for member in members:
        for vector in speaker_base_embedding_vectors[member.name]:
            speaker_embedding_vector[tuple(vector)] = member.name
            embedding_vectors_data.append(vector)
    
    
    
    audio_file_path = WAVE_OUTPUT_RESAMPLED_FILENAME
    audio_file_embedding = inference.get_embedding(audio_file_path, SPEAKER_RECOGNITION_MODEL)
    
    embedding_vector_distance = [(vector, inference.compute_distance(vector, audio_file_embedding)) for vector in embedding_vectors_data]
    sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])

    speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS]]
    print(speaker_predictions)
    predicted_speaker = Counter(speaker_predictions).most_common(1)[0][0]        

    print(predicted_speaker)
    
    import time
    
    start_time = time.time()
    # content = speech2text(WAVE_OUTPUT_RAW_FILENAME, SPEECH_RECOGNITION_MODEl)
    content = recognizer.recognize_google(WAVE_OUTPUT_RAW_FILENAME, language="vi-VN")
    end_time = time.time()
    print(end_time - start_time)
    print(content)
    
    action, device = extract_action_and_device(content)
    print(f"Action: {action} Device: {device}")
    
    if check_permission[predicted_speaker][device] == True:
        print(f"{predicted_speaker} có quyền")
        motor = MotorController(enable_pin=14, motor_pin1=15, motor_pin2=18, switch_pin_open=23, switch_pin_close=24)
        motor.open_door_close_door(3)
    else:
        print(f"{predicted_speaker} đéo có quyền")

    
        
    # if prediction == "Phạm Nguyễn Anh Phát" or prediction == "Lê Anh Tuấn":
    #     # Thiết lập chân GPIO
    #     ENABLE_PIN = 23
    #     IN1_PIN = 24
    #     IN2_PIN = 25
    #     SPEED = 50  # Tốc độ quay (từ 0 đến 100)

    #     # Tạo đối tượng điều khiển động cơ
    #     motor = MotorController(ENABLE_PIN, IN1_PIN, IN2_PIN)

    #     try:
    #         # Chạy động cơ tiến với tốc độ SPEED
    #         motor.forward(SPEED)
    #         time.sleep(2)  # Chạy trong 2 giây

    #         # Dừng động cơ
    #         motor.stop()
    #         time.sleep(1)  # Dừng trong 1 giây

    #         # Chạy động cơ lùi với tốc độ SPEED
    #         motor.backward(SPEED)
    #         time.sleep(2)  # Chạy trong 2 giây

    #         # Dừng động cơ
    #         motor.stop()

    #     except KeyboardInterrupt:
    #         # Dừng động cơ khi người dùng nhấn Ctrl+C
    #         motor.stop()
    #         GPIO.cleanup()  # Dọn dẹp GPIO

    #     finally:
    #         # Dọn dẹp GPIO khi kết thúc chương trình
    #         GPIO.cleanup()
    # elif prediction == "Trần Đức Trí":
    #     door_controller = ServoController(pin=15)
    #     # Open and close the door
    #     door_controller.open_door(0)
    #     time.sleep(3)  # Keep the door open for 3 seconds
    #     door_controller.close_door(110)
    # elif prediction == "Lê Văn Tiến Đạt":
    #     door_controller = ServoController(pin=18)
    #     # Open and close the door
    #     door_controller.open_door(0)
    #     time.sleep(3)  # Keep the door open for 3 seconds
    #     door_controller.close_door(110)

try:
    while True:
        if GPIO.input(26) == GPIO.LOW: # Nếu nút bấm được nhấn
            record_audio()
except KeyboardInterrupt:
    pass
finally:
    # Dọn dẹp GPIO và PyAudio
    GPIO.cleanup()
    audio.terminate()
