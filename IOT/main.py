import os
from dotenv import load_dotenv
from collections import defaultdict, Counter
import pyaudio
import wave
import RPi.GPIO as GPIO
from pydub import AudioSegment
import speech_recognition as sr
import numpy as np
import time

from db.db_helper import query_members, query_permissions, query_member_files, get_features, connect_db
from utils import convert_sample_rate, extract_action_and_device, speak_text, extend_audio

from devices.servo import ServoController
from devices.motor import MotorController
from devices.stepper import StepperController
from devices.led import Led
from devices.dht11 import DHTSensor
from devices.api import API
from devices.touch import TouchSensor

import speaker_recognition.neural_net as neural_net
import speaker_recognition.inference as inference

# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# SPEECH_RECOGNITION_MODEl = pipeline('automatic-speech-recognition', model='vinai/PhoWhisper-base', device=DEVICE)

# Tải các biến môi trường từ tệp .env
load_dotenv()

SPEAKER_RECOGNITION_MODEL_PATH = os.getenv("SPEAKER_RECOGNITION_MODEL_PATH")
SPEAKER_RECOGNITION_MODEL = neural_net.get_speaker_encoder(SPEAKER_RECOGNITION_MODEL_PATH)

DB_PATH = os.getenv("DB_PATH")
CONN = connect_db(DB_PATH)

N_TIMES_DUPLICATE = int(os.getenv("N_TIMES_DUPLICATE"))
N_TAKEN_AUDIO = int(os.getenv("N_TAKEN_AUDIO"))
K_NEAREST_NEIGHBOURS = int(os.getenv("K_NEAREST_NEIGHBOURS"))

# Thiết lập các tham số ghi âm
FORMAT = eval(os.getenv("FORMAT"))
CHANNELS = int(os.getenv("CHANNELS"))
RATE = int(os.getenv("RATE"))
CHUNK = int(os.getenv("CHUNK"))
RAW_RECORDING_PATH = os.getenv("RAW_RECORDING_PATH")
RESAMPLED_RATE = int(os.getenv("RESAMPLED_RATE"))

WAVE_OUTPUT_RAW_FILENAME = os.getenv("WAVE_OUTPUT_RAW_FILENAME")
WAVE_OUTPUT_RESAMPLED_FILENAME = os.getenv("WAVE_OUTPUT_RESAMPLED_FILENAME")

MAC_ADDRESS = os.getenv("MAC_ADDRESS")

motor = MotorController(enable_pin=14, motor_pin1=15, motor_pin2=18, switch_pin_open=3, switch_pin_close=24)
stepper = StepperController(pin1=21, pin2=20, pin3=16, pin4=12)
servo_parent = ServoController(pin=7)
servo_children = ServoController(pin=8)
led_living = Led(4)
led_kitchen = Led(17, 27)
led_children = Led(10, 9)
led_parent = Led(11)
led_garage = Led(5, 6)
dht = DHTSensor(13, 19, 26)
api = API(MAC_ADDRESS)
touch_sensor = TouchSensor(22)

status_data = {
    "Garage Led": 0,
    "Garage Door": 0,
    "Living Led": 0,
    "Kitchen Led": 0,
    "Parent Led": 0,
    "Children Led": 0,
    "Temperature": 0,
    "Humidity": 0,
}


# Khởi tạo đối tượng Recognizer
recognizer = sr.Recognizer()

# Khởi tạo PyAudio
audio = pyaudio.PyAudio()


# Khai báo chân GPIO cho servo
def record_audio():
    try:
        # Bắt đầu ghi âm
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        print("Recording...")

        frames = []
        start_time = time.time()
        while touch_sensor.is_touched(): # Ghi âm khi nút bấm được nhấn
            data = stream.read(CHUNK)
            frames.append(data)
            elapsed_time = time.time() - start_time
            print(f"Recording time: {elapsed_time:.2f} seconds", end="\r")

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

        try:
            convert_sample_rate(WAVE_OUTPUT_RAW_FILENAME, WAVE_OUTPUT_RESAMPLED_FILENAME, 16000)

            sound = AudioSegment.from_file(WAVE_OUTPUT_RESAMPLED_FILENAME, format="wav")
            duplicated_sound = sound * N_TIMES_DUPLICATE
            duplicated_sound.export(WAVE_OUTPUT_RESAMPLED_FILENAME, format="wav")
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return

        members = query_members(CONN)
        permissions = query_permissions(CONN)
        check_permission = defaultdict(lambda: defaultdict(lambda: False))
        for permission in permissions:
            check_permission[permission.member_name][permission.appliance_name] = True


        speaker_base_embedding_vectors = defaultdict(list)        
        for member in members:
            member_features = []
            for file in query_member_files(CONN, member.name):
                temp_vectors = get_features(file['features'])
                member_features.extend(temp_vectors)
            speaker_base_embedding_vectors[member.name] = member_features


        # for member in members:
        #     print(member.name, len(speaker_base_embedding_vectors[member.name]))


        # speaker_embedding_vector = defaultdict(lambda: "")
        # embedding_vectors_data = []

        # for member in members:
        #     for vector in speaker_base_embedding_vectors[member.name]:
        #         speaker_embedding_vector[tuple(vector)] = member.name
        #         embedding_vectors_data.append(vector)

        try:
            audio_file_embedding = inference.get_embedding(WAVE_OUTPUT_RESAMPLED_FILENAME, SPEAKER_RECOGNITION_MODEL)

            speaker_cosine_similarities = defaultdict(list)
            for member in members:
                speaker_cosine_similarities[member.name] = [inference.compute_cosine_similarity(vector, audio_file_embedding) for vector in speaker_base_embedding_vectors[member.name]]


            speaker_cosine_similarity = defaultdict(lambda:0)
            for member in members:
                speaker_cosine_similarity[member.name] = np.mean(speaker_cosine_similarities[member.name])

            for member in members:
                print(f"\033[94m {member.name}: {speaker_cosine_similarity[member.name]}\033[0m")

            predicted_speaker = min(speaker_cosine_similarity, key=speaker_cosine_similarity.get)

            print(f"\033[92mNgười được dự đoán: {predicted_speaker}\033[0m")


            # embedding_vector_distance = [(vector, inference.compute_distance(vector, audio_file_embedding)) for vector in embedding_vectors_data]
            # sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])

            # speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS]]
            # print(speaker_predictions)
            # predicted_speaker = Counter(speaker_predictions).most_common(1)[0][0]

            # print(predicted_speaker)
        except Exception as e:
            print(f"Error in speaker recognition: {e}")
            return

        try:
            with sr.AudioFile(WAVE_OUTPUT_RAW_FILENAME) as source:
                # Lắng nghe và nhận dạng âm thanh
                audio_data = recognizer.record(source)
                try:
                    # Sử dụng Google Web Speech API để nhận dạng văn bản từ âm thanh
                    content = recognizer.recognize_google(audio_data, language="vi-VN").lower()
                    print("Văn bản được nhận dạng: ", content)
                except sr.UnknownValueError:
                    print("Không thể nhận dạng văn bản từ âm thanh.")
                except sr.RequestError as e:
                    print("Lỗi trong quá trình gửi yêu cầu: ", e)
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return

        action, device = extract_action_and_device(content)
        print(f"Action: {action} Device: {device}")

        if check_permission[predicted_speaker][device] == True:
            if action == None or device == None:
                speak_text(f"Xin chào {predicted_speaker}. Thiết bị không nhận diện được")
                print(f"\033[92mXin chào {predicted_speaker}. Thiết bị không nhận diện được\033[0m")
            else:
                speak_text(f"Xin chào {predicted_speaker}. Bạn có quyền {action} {device}")
                print(f"\033[92m{predicted_speaker} có quyền\033[0m")

            try:
                if device == "cửa phòng khách":
                    motor.open_door_close_door(3)
                elif device == "cửa nhà xe":
                    if action == "mở":
                        stepper.rotate("forward", 5)
                        status_data["Garage Door"] = 1
                    else:
                        stepper.rotate("backward", 5)
                        status_data["Garage Door"] = 0
                elif device == "cửa phòng ngủ con cái":
                    servo_children.open_door_close_door(0, 6)
                elif device == "cửa phòng ngủ ba mẹ":
                    servo_parent.open_door_close_door(0, 6)
                elif device == "đèn phòng khách":
                    if action == "bật":
                        led_living.on()
                        status_data["Living Led"] = 1
                    else:
                        led_living.off()
                        status_data["Living Led"] = 0
                elif device == "đèn phòng bếp":
                    if action == "bật":
                        led_kitchen.on()
                        status_data["Kitchen Led"] = 1
                    else:
                        led_kitchen.off()
                        status_data["Kitchen Led"] = 0
                elif device == "đèn phòng ngủ ba mẹ":
                    if action == "bật":
                        led_parent.on()
                        status_data["Parent Led"] = 1
                    else:
                        led_parent.off()
                        status_data["Parent Led"] = 0
                elif device == "đèn phòng ngủ con cái":
                    if action == "bật":
                        led_children.on()
                        status_data["Children Led"] = 1
                    else:
                        led_children.off()
                        status_data["Children Led"] = 0
                elif device == "đèn nhà xe":
                    if action == "bật":
                        led_garage.on()
                        status_data["Garage Led"] = 1
                    else:
                        led_garage.off()
                        status_data["Garage Led"] = 0
                elif device == "cảm biến":
                    if action == "xem":
                        humidity, temperature = dht.read_dht11()
                        status_data["Humidity"] = humidity
                        status_data["Temperature"] = temperature
                        
                        speak_text(f"Nhiệt độ hiện tại là {temperature} độ C và độ ẩm là {humidity} %")

                api.send_data(status_data)
            except Exception as e:
                print(f"Error controlling device: {e}")

            print(f"\033[92mUpdate Screen!\033[0m")
        else:
            speak_text(f"Xin chào {predicted_speaker}. Bạn không có quyền {action} {device}")
            print(f"\033[91m{predicted_speaker} không có quyền có quyền\033[0m")
    except Exception as e:
        print(f"Error in record_audio: {e}")

try:

    # tri_folder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic/Trí"
    # phat_folder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic/Phát"
    # dat_folder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic/Đạt"
    # # tuan_folder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-new-model-mic/Tuấn"


    # tri_audio_files = [file for file in os.listdir(tri_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
    # phat_audio_files = [file for file in os.listdir(phat_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
    # dat_audio_files = [file for file in os.listdir(dat_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]
    # # # tuan_audio_files = [file for file in os.listdir(tuan_folder_path)[:N_TAKEN_AUDIO] if file.endswith(".wav")]

    # speaker_base_embedding_vectors = defaultdict(list)        

    # speaker_base_embedding_vectors["Trần Đức Trí"] = [inference.get_embedding(os.path.join(tri_folder_path, audio), SPEAKER_RECOGNITION_MODEL) for audio in tri_audio_files]
    # speaker_base_embedding_vectors["Phạm Nguyễn Anh Phát"] = [inference.get_embedding(os.path.join(phat_folder_path, audio), SPEAKER_RECOGNITION_MODEL) for audio in phat_audio_files]
    # speaker_base_embedding_vectors["Lê Văn Tiến Đạt"] = [inference.get_embedding(os.path.join(dat_folder_path, audio), SPEAKER_RECOGNITION_MODEL) for audio in dat_audio_files]
    print("Ready...")
    
    while True:
        if touch_sensor.is_touched(): # Nếu nút bấm được nhấn
            record_audio()
except KeyboardInterrupt:
    pass
finally:
    # Dọn dẹp GPIO và PyAudio
    GPIO.cleanup()
    audio.terminate()
