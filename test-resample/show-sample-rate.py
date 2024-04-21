import soundfile as sf

# Đường dẫn đến file âm thanh
tri_file = r"/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/test-resample/[Raspberry] [Trí] So sánh CPU và GPU.wav.wav"
phat_file = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\resample-phat.mp3"

# Đọc file âm thanh và lấy thông tin
data, sample_rate = sf.read(tri_file, dtype='float32')
print("Sample rate của Trí là:", sample_rate, "Hz")

# data, sample_rate = sf.read(phat_file, dtype='float32')
# print("Sample rate của Phát là:", sample_rate, "Hz")

