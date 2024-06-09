from pydub import AudioSegment
import os

# Đường dẫn file đầu vào
input_path = "D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\draft_audio_raspberry\TUAN_5_MINUTES_recording_resampled.wav"

# Thư mục lưu file đầu ra
output_dir = "D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\Tuấn-100-2.wav"
os.makedirs(output_dir, exist_ok=True)

# Đọc file audio đầu vào
audio = AudioSegment.from_wav(input_path)

# Độ dài mỗi đoạn (milliseconds)
segment_duration = 2000  # 2 giây
first_segment_duration = 100000  # 100 giây

# Chia file đầu tiên dài 100 giây
first_segment = audio[:first_segment_duration]
first_segment.export(os.path.join(output_dir, "Tuan_base_100s.wav"), format="wav")

# Chia các file tiếp theo, mỗi file dài 5 giây
for i in range(1, 101):
    start_time = first_segment_duration + (i - 1) * segment_duration
    end_time = start_time + segment_duration
    segment = audio[start_time:end_time]
    segment.export(os.path.join(output_dir, f"Tuan_segment_2s_{i}.wav"), format="wav")

print("Audio segments created successfully.")
