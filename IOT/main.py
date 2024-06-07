import os
from dotenv import load_dotenv
from collections import defaultdict, Counter
import pyaudio
import wave
import RPi.GPIO as GPIO
from pydub import AudioSegment
import speech_recognition as sr

from db.db_helper import query_members, query_permissions, query_member_files, get_features, connect_db
from utils import convert_sample_rate, extract_action_and_device, speak_text

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

        while touch_sensor.is_touched(): # Ghi âm khi nút bấm được nhấn
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

        try:
            convert_sample_rate(WAVE_OUTPUT_RAW_FILENAME, WAVE_OUTPUT_RESAMPLED_FILENAME, 16000)

            sound = AudioSegment.from_file(WAVE_OUTPUT_RESAMPLED_FILENAME, format="wav")
            duplicated_sound = sound * 5
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
            speaker_base_embedding_vectors[member.name] = [get_features(vector['features']) for vector in query_member_files(CONN, member.name)]
                
        speaker_embedding_vector = defaultdict(lambda: "")
        embedding_vectors_data = []
    
        for member in members:
            for vector in speaker_base_embedding_vectors[member.name]:
                speaker_embedding_vector[tuple(vector)] = member.name
                embedding_vectors_data.append(vector)
    
        try:
            audio_file_path = WAVE_OUTPUT_RESAMPLED_FILENAME
            audio_file_embedding = inference.get_embedding(audio_file_path, SPEAKER_RECOGNITION_MODEL)
    
            embedding_vector_distance = [(vector, inference.compute_distance(vector, audio_file_embedding)) for vector in embedding_vectors_data]
            sorted_embedding_vector_distance = sorted(embedding_vector_distance, key=lambda pair: pair[1])
    
            speaker_predictions = [speaker_embedding_vector[tuple(vector)] for vector, distance in sorted_embedding_vector_distance[:K_NEAREST_NEIGHBOURS]]
            print(speaker_predictions)
            predicted_speaker = Counter(speaker_predictions).most_common(1)[0][0]        
    
            print(predicted_speaker)
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
    
        if check_permission[predicted_speaker][device] == True or device == "cảm biến":
            speak_text(f"Xin chào {predicted_speaker}. Bạn có quyền {action} {device}")
            print(f"\033[92m{predicted_speaker} có quyền\033[0m")
    
            try:
                if device == "cửa phòng khách":
                    motor.open_door_close_door(3)
                elif device == "cửa nhà xe":
                    if action == "mở":
                        stepper.rotate("forward", 6)
                        status_data["Garage Door"] = 1
                    else:
                        stepper.rotate("backward", 6)
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
    while True:
        if touch_sensor.is_touched(): # Nếu nút bấm được nhấn
            record_audio()
except KeyboardInterrupt:
    pass
finally:
    # Dọn dẹp GPIO và PyAudio
    GPIO.cleanup()
    audio.terminate()
