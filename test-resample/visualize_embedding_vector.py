import neural_net
import inference
import numpy as np
import matplotlib.pyplot as plt


# Load pre-trained encoder
encoder_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\mfcc_lstm_model_360h_50000epochs_specaug_8batch_3stacks_cpu.pt"
encoder = neural_net.get_speaker_encoder(encoder_path)

phat_audio_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\resample-phat.mp3"
tri_audio_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\resample-tri.mp3"

# Nhúng file âm thanh
phat_audio_file_embedding = inference.get_embedding(phat_audio_path, encoder)
tri_audio_file_embedding = inference.get_embedding(tri_audio_path, encoder)

print(phat_audio_file_embedding)
print(tri_audio_file_embedding)


# Check if the arrays are equal element-wise
if np.array_equal(phat_audio_file_embedding, tri_audio_file_embedding):
    print("The two embedding vectors are the same.")
else:
    print("The two embedding vectors are different.")

# Plot the embedding vectors
plt.figure(figsize=(10, 6))
plt.plot(phat_audio_file_embedding, label='Phat Embedding', marker='o')
plt.plot(tri_audio_file_embedding, label='Tri Embedding', marker='o')
plt.title('Visualization of Embedding Vectors')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Plot the embedding vectors
axs[0].plot(phat_audio_file_embedding, label='Phat Embedding', marker='o')
axs[0].set_title('Phat Embedding')
axs[0].set_xlabel('Index')
axs[0].set_ylabel('Value')
axs[0].grid(True)

axs[1].plot(tri_audio_file_embedding, label='Tri Embedding', marker='o')
axs[1].set_title('Tri Embedding')
axs[1].set_xlabel('Index')
axs[1].set_ylabel('Value')
axs[1].grid(True)

plt.tight_layout()
plt.show()