from django.db import models
import os
from pydub import AudioSegment
import subprocess
import json
from .speaker_recognition import inference, neural_net
import numpy as np

BASE_DIR = os.path.dirname(os.getcwd())
ENCODER_PATH = os.path.join(BASE_DIR, "AI Module", "Speaker_Recognition", "LSTM", "saved_model", "train-clean-360-hours-50000-epochs-specaug-8-batch-3-stacks-cpu", "saved_model_20240324123652.ckpt-50000.pt")

def convert_audio_to_vector(ENCODER_PATH, audio_file_path):

    ENCODER = neural_net.get_speaker_encoder(ENCODER_PATH)
    
    audio_file_embedding = inference.get_embedding(audio_file_path, ENCODER)

    # Giả sử hàm này trích xuất đặc trưng từ file âm thanh và trả về một list chứa các float
    return audio_file_embedding  # Thay thế bằng code AI của bạn

# Đảm bảo rằng đường dẫn đến các thư mục tồn tại
def ensure_dir(file_path):
    dirctory = os.path.dirname(file_path)
    if not os.path.exists(dirctory):
        os.makedirs(dirctory)
        
def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    ensure_dir(output_path)  # Đảm bảo thư mục đầu ra tồn tại
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', input_path, '-ar', str(target_sample_rate), output_path]
    subprocess.run(command, check=True)
    

def member_audio_directory_path(instance, filename):
    # Trả về đường dẫn lưu trữ file cho từng thành viên
    return os.path.join('audio_raw_data', str(instance.member.name), filename)

class Member(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField('about', max_length=500, blank=True, default="Em là fan cứng ba Duy")
    
    def __str__(self):
        return self.name

class MemberFile(models.Model):
    member = models.ForeignKey(Member, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=member_audio_directory_path)
    features = models.TextField(blank=True, null=True)  # Lưu vector dưới dạng JSON

    def __str__(self):
        return f"{self.member.name} - File"
    
    def get_features(self):
        """Chuyển chuỗi JSON trở lại thành np.ndarray."""
        if self.features:
            # Đọc chuỗi JSON và chuyển nó thành một list
            features_list = json.loads(self.features)
            # Chuyển list thành np.ndarray
            return np.array(features_list)
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        file_name = os.path.basename(self.file.name)
        raw_audio_path = self.file.path
        resampled_audio_path = os.path.join('audio_resampled_data', str(self.member.name), file_name)
        
        # Resample audio
        convert_sample_rate(raw_audio_path, resampled_audio_path, 16000)
        
        # Nếu muốn ghép nối nhiều bản sao của âm thanh:
        sound = AudioSegment.from_file(resampled_audio_path, format="wav")
        duplicated_sound = sound * 5  # Tạo 5 bản sao và ghép chúng lại
        duplicated_sound.export(resampled_audio_path, format="wav")
        if not self.features:
            print("aaa")
            # Chỉ xử lý nếu chưa có vector
            extracted_features = convert_audio_to_vector(ENCODER_PATH, resampled_audio_path)
            features_list = extracted_features.tolist() if isinstance(extracted_features, np.ndarray) else extracted_features
            self.features = json.dumps(features_list)  # Convert list to JSON string
            super().save(*args, **kwargs)
