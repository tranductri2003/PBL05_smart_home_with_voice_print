import os
from pydub import AudioSegment

# Đảm bảo rằng đường dẫn đến các thư mục tồn tại
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def convert_to_16000_sampling_rate(input_path, output_path):
    ensure_dir(output_path)  # Đảm bảo thư mục đầu ra tồn tại
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_frame_rate(16000)
    sound.export(output_path, format="wav")