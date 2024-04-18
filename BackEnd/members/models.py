from django.db import models
import os
from pydub import AudioSegment

# Đảm bảo rằng đường dẫn đến các thư mục tồn tại
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    ensure_dir(output_path)  # Đảm bảo thư mục đầu ra tồn tại
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_frame_rate(target_sample_rate)
    sound.export(output_path, format="wav")


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
    
    def __str__(self):
        return f"{self.member.name} - File"
    
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
