from pydub import AudioSegment

def convert_to_16000_sampling_rate(input_path, output_path):
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_frame_rate(16000)
    sound.export(output_path, format="wav")


convert_to_16000_sampling_rate(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\k sử dụng mic.mp3", "fuck.wav")