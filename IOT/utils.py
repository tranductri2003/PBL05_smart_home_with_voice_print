import subprocess
import re
from gtts import gTTS
import pygame
import os

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', input_path, '-ar', str(target_sample_rate), output_path]
    subprocess.run(command, check=True)

def speech2text(wav_file, model):
    return model(wav_file)['text']

# Function to extract action and device
def extract_action_and_device(sentence):
    # Updated regular expression pattern
    pattern = r"(mở|đóng|bật|tắt|xem)\s+(cửa nhà xe|đèn nhà xe|cửa phòng khách|đèn phòng khách|cửa phòng ngủ ba mẹ|đèn phòng ngủ ba mẹ|cửa phòng ngủ con cái|đèn phòng ngủ con cái|đèn phòng bếp|cảm biến)\b"

    match = re.search(pattern, sentence)
    if match:
        action = match.group(1).strip()
        device = match.group(2).strip()
        return action, device
    else:
        return None, None

def speak_text(text, lang='vi', volume=1.0):
    # Sử dụng gTTS để chuyển văn bản thành giọng nói
    tts = gTTS(text=text, lang=lang, slow=False)

    # Lưu giọng nói vào một file tạm thời
    tts.save("temp.mp3")

    # Khởi tạo pygame mixer
    pygame.mixer.init()

    # Tải và phát file âm thanh
    pygame.mixer.music.load("temp.mp3")
    
    # Tăng âm lượng
    pygame.mixer.music.set_volume(volume)

    pygame.mixer.music.play()

    # Chờ cho đến khi phát xong
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Xóa file tạm
    os.remove("temp.mp3")


    
"""
Tôi muốn mở cửa cuốn nhà xe
Tôi muốn đóng cửa cuốn nhà xe
Tôi muốn bật đèn nhà xe
Tôi muốn tắt đèn nhà xe

Tôi muốn mở cửa trượt phòng khách
Tôi muốn bật đèn phòng khách
Tôi muốn tắt đèn phòng khách

Tôi muốn mở cửa phòng ngủ ba mẹ
Tôi muốn bật đèn phòng ngủ ba mẹ
Tôi muốn tắt đèn phòng ngủ ba mẹ

Tôi muốn mở cửa phòng ngủ con cái
Tôi muốn bật đèn phòng ngủ con cái
Tôi muốn tắt đèn phòng ngủ con cái

Tôi muốn bật đèn phòng bếp
Tôi muốn tắt đèn phòng bếp

Tôi muốn xem cảm biến
"""

