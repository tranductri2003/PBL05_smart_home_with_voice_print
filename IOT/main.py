import os
from collections import defaultdict, Counter
import Speaker_Recognition.neural_net
import Speaker_Recognition.inference
import Speaker_Recognition.myconfig
import Speaker_Recognition.dataset
import Speaker_Recognition.feature_extraction
import Speaker_Recognition.specaug
import time
import pyaudio
import wave
import RPi.GPIO as GPIO
import librosa
import soundfile as sf
import subprocess
from pydub import AudioSegment

from db_helper import Member, Appliance, Permission, query_members, query_appliances, query_permissions, connect_db
from utils import convert_to_16000_sampling_rate


        

    
ENCODER_PATH = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\IOT\Speaker_Recognition\saved_model\train-clean-360-hours-50000-epochs-specaug-8-batch-4-stacks-cpu"   
ENCODER = Speaker_Recognition.neural_net.get_speaker_encoder(ENCODER_PATH)

SPEAKER_RESAMPLED_DATA_PATH = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\BackEnd\audio_resampled_data"
DB_PATH = r"D:\\Code\\BachKhoa\\PBL 5\\PBL05_smart_home_with_voice_print_and_antifraud_ai\\BackEnd\\db.sqlite3"
CONN = connect_db(DB_PATH)

N_TAKEN_AUDIO = 5
K_NEAREST_NEIGHBOURS = 5

# Thiết lập các tham số ghi âm
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512 
RAW_RECORDING_PATH = "./temp_recorded_audio/recording.wav"
RESAMPLED_RECORDING_PATH = "./temp_recorded_audio/recording_resampled.wav"
RESAMPLED_RATE = 16000  # Tần số lấy mẫu mới


SERVO_PIN = 26

# Khởi tạo PyAudio
audio = pyaudio.PyAudio()

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 14 là chân được kết nối với nút bấm
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Khai báo đối tượng PWM
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz (chu kỳ 20ms) là tần số tiêu chuẩn cho servo

def set_angle(angle):
    duty = angle / 18 + 2  # Chuyển đổi góc sang chu kỳ
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

# Hàm để kiểm soát servo khi nhận diện được "Phát"
def control_servo():
    pwm.start(0)  # Khởi động PWM
    set_angle(90)  # Quay servo 90 độ
    time.sleep(0.5)  # Chờ 0.5 giây
    set_angle(0)  # Quay servo về góc 0 độ
    
    
# Khai báo chân GPIO cho servo
def record_audio():
    # Bắt đầu ghi âm
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    while GPIO.input(14) == GPIO.LOW: # Ghi âm khi nút bấm được nhấn
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Dừng ghi âm
    stream.stop_stream()
    stream.close()

    # Lưu âm thanh vào file WAV
    with wave.open(RAW_RECORDING_PATH, 'wb') as wf:
        RESAMPLED_RECORDING_PATH = "./temp_recorded_audio/recording_resampled.wav"
    
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    
    convert_to_16000_sampling_rate(RAW_RECORDING_PATH, RESAMPLED_RECORDING_PATH)

    
    sound = AudioSegment.from_file(RESAMPLED_RECORDING_PATH, format="wav")
    duplicated_sound = sound * 5  # Tạo 5 bản sao và ghép chúng lại
    duplicated_sound.export(RESAMPLED_RECORDING_PATH, format="wav")    
    
    
    
    
    members = query_members(CONN)
    appliances = query_appliances(CONN)
    permissions = query_permissions(CONN)
    
    speaker_folder_path = defaultdict(lambda: "")
    for member in members:
        speaker_folder_path[member.name] = os.path.join(SPEAKER_RESAMPLED_DATA_PATH, member.name)
        
    speaker_audio_files = defaultdict(list)
    for member in members:
        speaker_audio_files[member.name] = [file for file in os.listdir(speaker_folder_path[member.name])]
        
    speaker_base_embedding_vectors = defaultdict(list)
    for member in members:
        speaker_base_embedding_vectors[member.name] = [Speaker_Recognition.inference.get_embedding(os.path.join(speaker_folder_path[member.name], audio), ENCODER) for audio in speaker_audio_files[member.name]]
        
    print(len(speaker_base_embedding_vectors[members[0].name]), len(speaker_base_embedding_vectors[members[0].name][0]))
        
    speaker_embedding_vector = defaultdict(lambda: "")
    embedding_vectors_data = []
    
    for member in members:
        for vector in speaker_base_embedding_vectors[member.name]:
            speaker_embedding_vector[tuple(vector)] = member.name
            embedding_vectors_data.append(vector)
    
    
    
    audio_file_path = RESAMPLED_RECORDING_PATH
    audio_file_embedding = Speaker_Recognition.inference.get_embedding(audio_file_path)
    
    embedding_vector_distance = [(vector, Speaker_Recognition.inference.compute_distance(vector, audio_file_embedding)) for vector in embedding_vectors_data]
    sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])

    speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS]]

    prediction = Counter(speaker_predictions).most_common(1)[0][0]        

    print(speaker_predictions)