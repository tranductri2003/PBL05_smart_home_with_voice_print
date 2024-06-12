import subprocess
import re
from gtts import gTTS
import pygame
import os
from pydub import AudioSegment

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', input_path, '-ar', str(target_sample_rate), output_path]
    subprocess.run(command, check=True)

def speech2text(wav_file, model):
    return model(wav_file)['text']

def extend_audio(audio, times=5):
    return audio * times

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

def count_files_in_folder(folder_path, extension=None):
    """
    Đếm số lượng file trong thư mục. Có thể đếm toàn bộ file hoặc chỉ file với đuôi mở rộng cụ thể.

    Parameters:
    folder_path (str): Đường dẫn đến thư mục cần kiểm tra.
    extension (str, optional): Đuôi mở rộng của file cần đếm (ví dụ: '.wav'). Nếu không có, đếm tất cả các file.

    Returns:
    int: Số lượng file trong thư mục.
    """
    if extension:
        return len([file for file in os.listdir(folder_path) if file.endswith(extension)])
    else:
        return len(os.listdir(folder_path))
    
def split_audio(input_path, output_dir, first_segment_duration, segment_duration, num_segments):
    """
    Splits an audio file into multiple segments and saves them to the output directory.
    
    Args:
    - input_path (str): Path to the input WAV file.
    - output_dir (str): Directory where the output segments will be saved.
    - first_segment_duration (int): Duration of the first segment in milliseconds.
    - segment_duration (int): Duration of each subsequent segment in milliseconds.
    - num_segments (int): Number of subsequent segments to create.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the input audio file
    audio = AudioSegment.from_wav(input_path)

    # Create the first segment
    first_segment = audio[:first_segment_duration]
    first_segment.export(os.path.join(output_dir, "Dat_base_100s.wav"), format="wav")

    # Create subsequent segments
    for i in range(1, num_segments + 1):
        start_time = first_segment_duration + (i - 1) * segment_duration
        end_time = start_time + segment_duration
        segment = audio[start_time:end_time]
        segment.export(os.path.join(output_dir, f"Dat_segment_3s_{i}.wav"), format="wav")

    print("Audio segments created successfully.")
    
def merge_audio_files(folder_path, output_file):
    # Khởi tạo một đối tượng âm thanh trống
    combined_audio = AudioSegment.empty()

    # Lặp qua tất cả các file trong thư mục
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.wav'):  # Chỉ xử lý các file .wav
            file_path = os.path.join(folder_path, filename)
            audio = AudioSegment.from_wav(file_path)
            combined_audio += audio

    # Xuất file âm thanh hợp nhất
    combined_audio.export(output_file, format="wav")
    print(f"All audio files have been merged into {output_file}")
    
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

