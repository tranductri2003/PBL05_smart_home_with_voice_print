from django.db import models
import os
from pydub import AudioSegment
import subprocess
import json
from .speaker_recognition import inference, neural_net
import numpy as np

BASE_DIR = os.path.dirname(os.getcwd())
ENCODER_PATH = os.path.join(BASE_DIR, "AI Module", "Speaker_Recognition", "LSTM", "saved_model", "saved_model_20240606215142.pt")

def convert_audio_to_vector(ENCODER_PATH, audio_file_path):
    ENCODER = neural_net.get_speaker_encoder(ENCODER_PATH)

    audio_file_embedding = inference.get_embedding(audio_file_path, ENCODER)
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
            return [np.array(features) for features in features_list]
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        file_name = os.path.basename(self.file.name)
        raw_audio_path = self.file.path
        resampled_audio_dir = os.path.join('audio_resampled_data', str(self.member.name))
        os.makedirs(resampled_audio_dir, exist_ok=True)
        
        # Resample audio
        resampled_audio_path = os.path.join(resampled_audio_dir, file_name)
        convert_sample_rate(raw_audio_path, resampled_audio_path, 16000)
        
        # Chia file thành các đoạn nhỏ 3 giây
        sound = AudioSegment.from_file(resampled_audio_path, format="wav")
        segment_duration = 3000  # 3 giây tính bằng milliseconds
        segments = [sound[i:i+segment_duration] for i in range(0, len(sound), segment_duration)]

        # Lưu các feature của từng đoạn nhỏ
        all_features = []

        for i, segment in enumerate(segments):
            segment_path = os.path.join(resampled_audio_dir, f"{file_name}_segment_{i}.wav")
            segment.export(segment_path, format="wav")
            
            # Extract features for this segment
            extracted_features = convert_audio_to_vector(ENCODER_PATH, segment_path)
            features_list = extracted_features.tolist() if isinstance(extracted_features, np.ndarray) else extracted_features
            all_features.append(features_list)

        # Lưu list các list feature dưới dạng JSON
        self.features = json.dumps(all_features)
        super().save(*args, **kwargs)
        
        # Xóa file âm thanh gốc và file resampled đầy đủ
        if os.path.exists(raw_audio_path):
            os.remove(raw_audio_path)
        if os.path.exists(resampled_audio_path):
            os.remove(resampled_audio_path)