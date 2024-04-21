import neural_net
import inference
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_frame_rate(target_sample_rate)
    sound.export(output_path, format="wav")

# Chuyển đổi mẫu âm thanh sang mẫu có tần số lấy mẫu mục tiêu
convert_sample_rate(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Đạt] Chiều cao trung bình cầu thủ.wav", r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Đạt] Chiều cao trung bình cầu thủ.wav", 16000)
convert_sample_rate(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Trí] Chiều cao trung bình cầu thủ.wav", r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Trí] Chiều cao trung bình cầu thủ.wav", 16000)
convert_sample_rate(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Trí] So sánh CPU và GPU.wav", r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Trí] So sánh CPU và GPU.wav", 16000)

# Đường dẫn đến encoder đã được huấn luyện trước
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt"
# Tải encoder đã được huấn luyện trước
encoder = neural_net.get_speaker_encoder(encoder_path)

# Đường dẫn đến các file âm thanh
dat_chieu_cao_cau_thu_audio_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Đạt] Chiều cao trung bình cầu thủ.wav"
tri_chieu_cao_cau_thu_audio_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Trí] Chiều cao trung bình cầu thủ.wav"
tri_so_sanh_cpu_gpu_audio_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\[Trí] So sánh CPU và GPU.wav"

# Nhúng các file âm thanh
dat_chieu_cao_cau_thu_embedding = inference.get_embedding(dat_chieu_cao_cau_thu_audio_path, encoder)
tri_chieu_cao_cau_thu_embedding = inference.get_embedding(tri_chieu_cao_cau_thu_audio_path, encoder)
tri_so_sanh_cpu_gpu_embedding = inference.get_embedding(tri_so_sanh_cpu_gpu_audio_path, encoder)

# In ra embedding vectors
print("Embedding vector of 'Dat Chieu cao cau thu':", dat_chieu_cao_cau_thu_embedding)
print("Embedding vector of 'Tri Chieu cao cau thu':", tri_chieu_cao_cau_thu_embedding)
print("Embedding vector of 'Tri So sanh CPU GPU':", tri_so_sanh_cpu_gpu_embedding)

# Vẽ biểu đồ embedding vectors
plt.figure(figsize=(10, 6))
plt.plot(tri_chieu_cao_cau_thu_embedding, label='Tri Chieu cao cau thu', marker='o')
plt.plot(tri_so_sanh_cpu_gpu_embedding, label='Tri So sanh CPU GPU', marker='o')
plt.title('Visualization of Embedding Vectors (Tri)')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()

# Vẽ biểu đồ embedding vectors
plt.figure(figsize=(10, 6))
plt.plot(dat_chieu_cao_cau_thu_embedding, label='Dat Chieu cao cau thu', marker='o')
plt.plot(tri_chieu_cao_cau_thu_embedding, label='Tri Chieu cao cau thu', marker='o')
plt.title('Visualization of Embedding Vectors (Dat and Tri Chieu cao cau thu)')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()

# Vẽ biểu đồ embedding vectors
plt.figure(figsize=(10, 6))
plt.plot(dat_chieu_cao_cau_thu_embedding, label='Dat Chieu cao cau thu', marker='o')
plt.plot(tri_so_sanh_cpu_gpu_embedding, label='Tri So sanh CPU GPU', marker='o')
plt.title('Visualization of Embedding Vectors (Dat and Tri So sanh CPU GPU)')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()


# Vẽ biểu đồ embedding vectors
plt.figure(figsize=(10, 6))
plt.plot(dat_chieu_cao_cau_thu_embedding, label='Dat Chieu cao cau thu', marker='o')
plt.plot(tri_chieu_cao_cau_thu_embedding, label='Tri Chieu cao cau thu', marker='o')
plt.plot(tri_so_sanh_cpu_gpu_embedding, label='Tri So sanh CPU GPU', marker='o')
plt.title('Visualization of Embedding Vectors (Dat, Tri Chieu cao cau thu, and Tri So sanh CPU GPU)')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()


# Tính cosine similarity giữa các cặp vector
similarity_tri_chieu_cao_cau_thu_tri_cpu_gpu = cosine_similarity(tri_chieu_cao_cau_thu_embedding.reshape(1, -1), tri_so_sanh_cpu_gpu_embedding.reshape(1, -1))
similarity_tri_chieu_cao_cau_thu_dat_chieu_cao_cau_thu = cosine_similarity(tri_chieu_cao_cau_thu_embedding.reshape(1, -1), dat_chieu_cao_cau_thu_embedding.reshape(1, -1))
similarity_tri_cpu_gpu_dat_chieu_cao_cau_thu = cosine_similarity(tri_so_sanh_cpu_gpu_embedding.reshape(1, -1), dat_chieu_cao_cau_thu_embedding.reshape(1, -1))

# In ra kết quả
print("Cosine similarity between Tri chieu cao cau thu and Tri so sanh CPU GPU:", similarity_tri_chieu_cao_cau_thu_tri_cpu_gpu)
print("Cosine similarity between Tri chieu cao cau thu and Dat chieu cao cau thu:", similarity_tri_chieu_cao_cau_thu_dat_chieu_cao_cau_thu)
print("Cosine similarity between Tri so sanh CPU GPU and Dat chieu cao cau thu:", similarity_tri_cpu_gpu_dat_chieu_cao_cau_thu)

# Tính khoảng cách Euclidean giữa các cặp vector
distance_tri_chieu_cao_cau_thu_tri_cpu_gpu = euclidean_distances(tri_chieu_cao_cau_thu_embedding.reshape(1, -1), tri_so_sanh_cpu_gpu_embedding.reshape(1, -1))
distance_tri_chieu_cao_cau_thu_dat_chieu_cao_cau_thu = euclidean_distances(tri_chieu_cao_cau_thu_embedding.reshape(1, -1), dat_chieu_cao_cau_thu_embedding.reshape(1, -1))
distance_tri_cpu_gpu_dat_chieu_cao_cau_thu = euclidean_distances(tri_so_sanh_cpu_gpu_embedding.reshape(1, -1), dat_chieu_cao_cau_thu_embedding.reshape(1, -1))

# In ra kết quả
print("Euclidean distance between Tri chieu cao cau thu and Tri so sanh CPU GPU:", distance_tri_chieu_cao_cau_thu_tri_cpu_gpu)
print("Euclidean distance between Tri chieu cao cau thu and Dat chieu cao cau thu:", distance_tri_chieu_cao_cau_thu_dat_chieu_cao_cau_thu)
print("Euclidean distance between Tri so sanh CPU GPU and Dat chieu cao cau thu:", distance_tri_cpu_gpu_dat_chieu_cao_cau_thu)
