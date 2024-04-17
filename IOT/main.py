import pyaudio
import wave
import RPi.GPIO as GPIO
import librosa
import soundfile as sf

import os
import torch
import neural_net
import time
import inference
import myconfig
import csv

import subprocess


# Load pre-trained encoder
encoder_path = r"/home/tranductri2003/Code/speaker-recognition-using-lstm/saved_model/train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-cpu/mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)


tri_base_embedding = inference.get_embedding(r"/home/tranductri2003/Code/speaker-recognition-using-lstm/Data Tiếng nói base/Trí/tri_1.wav", encoder)
dat_base_embedding = inference.get_embedding(r"/home/tranductri2003/Code/speaker-recognition-using-lstm/Data Tiếng nói base/Đạt/DAT_1.wav", encoder)
tuan_base_embedding = inference.get_embedding(r"/home/tranductri2003/Code/speaker-recognition-using-lstm/Data Tiếng nói base/Tuấn/tuan_0.wav", encoder)
phat_base_embedding = inference.get_embedding(r"/home/tranductri2003/Code/speaker-recognition-using-lstm/Data Tiếng nói base/Phát/phat_1.wav", encoder)


import pyaudio
import wave
import RPi.GPIO as GPIO
import librosa
import soundfile as sf

import subprocess


# Load pre-trained encoder
encoder_path = r"/home/tranductri2003/Code/speaker-recognition-using-lstm/saved_model/train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-cpu/mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)

# Thiết lập các tham số ghi âm
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512 
WAVE_OUTPUT_FILENAME = "recording.wav"
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
    
def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', input_path, '-ar', str(target_sample_rate), output_path]
    subprocess.run(command, check=True)
    
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
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Đọc âm thanh từ file ghi âm
    y, sr = librosa.load(WAVE_OUTPUT_FILENAME, sr=None)

    # Đường dẫn của tập tin ghi âm ban đầu
    input_path = 'recording.wav'
    # Đường dẫn của tập tin sau khi resample
    output_path = 'resampled_recording.wav'

    # Chuyển đổi tần số lấy mẫu của tệp ghi âm
    convert_sample_rate(input_path, output_path, RESAMPLED_RATE)

    # Đọc âm thanh từ tệp resampled
    y_resampled, sr_resampled = librosa.load(output_path, sr=None)

    # Ghi âm thanh resampled vào file mới
    sf.write(output_path, y_resampled, RESAMPLED_RATE)

    audio_file_path = output_path
    
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
    
    print(f"Nhận diện được: {prediction}")
    
    if prediction == "Phát":
        control_servo()


try:
    while True:
        if GPIO.input(14) == GPIO.LOW: # Nếu nút bấm được nhấn
            record_audio()
except KeyboardInterrupt:
    pass
finally:
    # Dọn dẹp GPIO và PyAudio
    GPIO.cleanup()
    audio.terminate()
