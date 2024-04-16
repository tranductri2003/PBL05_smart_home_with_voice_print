import subprocess
import os
import tensorflow as tf

DATASET_AUDIO_PATH = r'D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\AI Module\Speaker_Recognition\LSTM\Data Tiếng nói base\Tuấn_2'  # Hãy thay thế bằng đường dẫn thực tế của dữ liệu
SAMPLING_RATE = 16000

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', input_path, '-ar', str(target_sample_rate), output_path]
    subprocess.run(command, check=True)

# Duyệt qua cấu trúc thư mục và chuyển đổi mỗi tệp
for root, dirs, files in os.walk(DATASET_AUDIO_PATH):
    for file in files:
        if file.endswith('.wav'):
            file_path = os.path.join(root, file)
            # print(file_path)
            # Lưu tạm thời tệp đã chuyển đổi
            temp_path = file_path + '.temp.wav'
            convert_sample_rate(file_path, temp_path, SAMPLING_RATE)
            # Thay thế tệp gốc bằng tệp đã chuyển đổi
            os.replace(temp_path, file_path)

print("Hoàn thành chuyển đổi.")
