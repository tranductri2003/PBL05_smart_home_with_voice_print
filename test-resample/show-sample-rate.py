import soundfile as sf

# Đường dẫn đến file âm thanh
file_path = r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\BackEnd\audio_resampled_data\Trần Đức Trí\tri_1.mp3"

# Đọc file âm thanh và lấy thông tin
data, sample_rate = sf.read(file_path, dtype='float32')
print("Sample rate của file là:", sample_rate, "Hz")
