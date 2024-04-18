from pydub import AudioSegment

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_frame_rate(target_sample_rate)
    sound.export(output_path, format="wav")


convert_sample_rate(r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\test-resample.mp3", r"D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\test-resample\resample-phat.mp3", 16000)