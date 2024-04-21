import neural_net
import inference
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

# ANSI escape codes for colors
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    
def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_frame_rate(target_sample_rate)
    sound.export(output_path, format="wav")

# Chuyển đổi mẫu âm thanh sang mẫu có tần số lấy mẫu mục tiêu
# convert_sample_rate(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Laptop] [Đạt] Chiều cao trung bình cầu thủ.wav", 16000)
# convert_sample_rate(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Laptop] [Trí] Chiều cao trung bình cầu thủ.wav", 16000)
# convert_sample_rate(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Laptop] [Trí] So sánh CPU và GPU.wav", 16000)
# convert_sample_rate(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Raspberry] [Trí] Chiều cao trung bình cầu thủ.wav", r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Raspberry] [Trí] Chiều cao trung bình cầu thủ.wav", 16000)
convert_sample_rate(r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Raspberry] [Trí] So sánh CPU và GPU.wav.wav", r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Raspberry] [Trí] So sánh CPU và GPU.wav.wav", 16000)

# Đường dẫn đến encoder đã được huấn luyện trước
encoder_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt"
# Tải encoder đã được huấn luyện trước
encoder = neural_net.get_speaker_encoder(encoder_path)

# Đường dẫn đến các file âm thanh
laptop_dat_chieu_cao_cau_thu_audio_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Laptop] [Đạt] Chiều cao trung bình cầu thủ.wav"
laptop_tri_chieu_cao_cau_thu_audio_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Laptop] [Trí] Chiều cao trung bình cầu thủ.wav"
laptop_tri_so_sanh_cpu_gpu_audio_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Laptop] [Trí] So sánh CPU và GPU.wav"
raspberry_tri_chieu_cao_cau_thu_audio_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Raspberry] [Trí] Chiều cao trung bình cầu thủ.wav"
raspberry_tri_so_sanh_cpu_gpu_audio_path = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Raspberry] [Trí] So sánh CPU và GPU.wav.wav"

# Nhúng các file âm thanh
laptop_dat_chieu_cao_cau_thu_embedding = inference.get_embedding(laptop_dat_chieu_cao_cau_thu_audio_path, encoder)
laptop_tri_chieu_cao_cau_thu_embedding = inference.get_embedding(laptop_tri_chieu_cao_cau_thu_audio_path, encoder)
laptop_tri_so_sanh_cpu_gpu_embedding = inference.get_embedding(laptop_tri_so_sanh_cpu_gpu_audio_path, encoder)
raspberry_tri_chieu_cao_cau_thu_embedding = inference.get_embedding(raspberry_tri_chieu_cao_cau_thu_audio_path, encoder)
raspberry_tri_so_sanh_cpu_gpu_embedding = inference.get_embedding(raspberry_tri_so_sanh_cpu_gpu_audio_path, encoder)

# In ra embedding vectors với màu tên người và tên thiết bị
print(Color.BOLD + "Embedding vector of '" + Color.BLUE + "laptop_Dat Chieu cao cau thu" + Color.ENDC + "':", laptop_dat_chieu_cao_cau_thu_embedding)
print(Color.BOLD + "Embedding vector of '" + Color.GREEN + "laptop_Tri Chieu cao cau thu" + Color.ENDC + "':", laptop_tri_chieu_cao_cau_thu_embedding)
print(Color.BOLD + "Embedding vector of '" + Color.WARNING + "laptop_Tri So sanh CPU GPU" + Color.ENDC + "':", laptop_tri_so_sanh_cpu_gpu_embedding)
print(Color.BOLD + "Embedding vector of '" + Color.BLUE + "raspberry_Tri Chieu cao cau thu" + Color.ENDC + "':", raspberry_tri_chieu_cao_cau_thu_embedding)
print(Color.BOLD + "Embedding vector of '" + Color.GREEN + "raspberry_Tri So sanh CPU GPU" + Color.ENDC + "':", raspberry_tri_so_sanh_cpu_gpu_embedding)


# Tính cosine similarity giữa các cặp vector
similarity_laptop_tri_chieu_cao_cau_thu_raspberry_tri_chieu_cao_cau_thu = cosine_similarity(laptop_tri_chieu_cao_cau_thu_embedding.reshape(1, -1), raspberry_tri_chieu_cao_cau_thu_embedding.reshape(1, -1))
similarity_laptop_tri_so_sanh_cpu_gpu_raspberry_tri_chieu_cao_cau_thu = cosine_similarity(laptop_tri_so_sanh_cpu_gpu_embedding.reshape(1, -1), raspberry_tri_chieu_cao_cau_thu_embedding.reshape(1, -1))
similarity_laptop_dat_chieu_cao_cau_thu_raspberry_tri_chieu_cao_cau_thu = cosine_similarity(laptop_dat_chieu_cao_cau_thu_embedding.reshape(1, -1), raspberry_tri_chieu_cao_cau_thu_embedding.reshape(1, -1))
similarity_rasberry_tri_so_sanh_cpu_gpu_raspberry_tri_chieu_cao_cau_thu = cosine_similarity(raspberry_tri_so_sanh_cpu_gpu_embedding.reshape(1, -1), raspberry_tri_chieu_cao_cau_thu_embedding.reshape(1, -1))

# In ra kết quả với màu
print(Color.BOLD + "Cosine similarity between " + Color.BLUE + "Laptop Tri chieu cao cau thu" + Color.ENDC + " and " + Color.BLUE + "Raspberry Tri chieu cao cau thu" + Color.ENDC + ":", similarity_laptop_tri_chieu_cao_cau_thu_raspberry_tri_chieu_cao_cau_thu)
print(Color.BOLD + "Cosine similarity between " + Color.GREEN + "Laptop Tri so sanh CPU GPU" + Color.ENDC + " and " + Color.BLUE + "Raspberry Tri chieu cao cau thu" + Color.ENDC + ":", similarity_laptop_tri_so_sanh_cpu_gpu_raspberry_tri_chieu_cao_cau_thu)
print(Color.BOLD + "Cosine similarity between " + Color.WARNING + "Laptop Dat chieu cao cau thu" + Color.ENDC + " and " + Color.BLUE + "Raspberry Tri chieu cao cau thu" + Color.ENDC + ":", similarity_laptop_dat_chieu_cao_cau_thu_raspberry_tri_chieu_cao_cau_thu)
print(Color.BOLD + "Cosine similarity between " + Color.BLUE + "Raspberry Tri so sanh CPU GPU" + Color.ENDC + " and " + Color.BLUE + "Raspberry Tri chieu cao cau thu" + Color.ENDC + ":", similarity_rasberry_tri_so_sanh_cpu_gpu_raspberry_tri_chieu_cao_cau_thu)

distance_laptop_tri_chieu_cao_cau_thu_raspberry_tri_chieu_cao_cau_thu = euclidean_distances(laptop_tri_chieu_cao_cau_thu_embedding.reshape(1, -1), raspberry_tri_chieu_cao_cau_thu_embedding.reshape(1, -1))
distance_laptop_tri_so_sanh_cpu_gpu_raspberry_tri_chieu_cao_cau_thu = euclidean_distances(laptop_tri_so_sanh_cpu_gpu_embedding.reshape(1, -1), raspberry_tri_chieu_cao_cau_thu_embedding.reshape(1, -1))
distance_laptop_dat_chieu_cao_cau_thu_raspberry_tri_chieu_cao_cau_thu = euclidean_distances(laptop_dat_chieu_cao_cau_thu_embedding.reshape(1, -1), raspberry_tri_chieu_cao_cau_thu_embedding.reshape(1, -1))
distance_rasberry_tri_so_sanh_cpu_gpu_raspberry_tri_chieu_cao_cau_thu = euclidean_distances(raspberry_tri_so_sanh_cpu_gpu_embedding.reshape(1, -1), raspberry_tri_chieu_cao_cau_thu_embedding.reshape(1, -1))

print(Color.BOLD + "Euclidean distance between " + Color.BLUE + "Laptop Tri chieu cao cau thu" + Color.ENDC + " and " + Color.BLUE + "Raspberry Tri chieu cao cau thu" + Color.ENDC + ":", distance_laptop_tri_chieu_cao_cau_thu_raspberry_tri_chieu_cao_cau_thu)
print(Color.BOLD + "Euclidean distance between " + Color.GREEN + "Laptop Tri so sanh CPU GPU" + Color.ENDC + " and " + Color.BLUE + "Raspberry Tri chieu cao cau thu" + Color.ENDC + ":", distance_laptop_tri_so_sanh_cpu_gpu_raspberry_tri_chieu_cao_cau_thu)
print(Color.BOLD + "Euclidean distance between " + Color.WARNING + "Laptop Dat chieu cao cau thu" + Color.ENDC + " and " + Color.BLUE + "Raspberry Tri chieu cao cau thu" + Color.ENDC + ":", distance_laptop_dat_chieu_cao_cau_thu_raspberry_tri_chieu_cao_cau_thu)
print(Color.BOLD + "Euclidean distance between " + Color.BLUE + "Raspberry Tri so sanh CPU GPU" + Color.ENDC + " and " + Color.BLUE + "Raspberry Tri chieu cao cau thu" + Color.ENDC + ":", distance_rasberry_tri_so_sanh_cpu_gpu_raspberry_tri_chieu_cao_cau_thu)