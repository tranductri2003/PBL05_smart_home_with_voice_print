from pydub import AudioSegment

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    sound = AudioSegment.from_file(input_path)
    sound = sound.set_frame_rate(target_sample_rate)
    sound.export(output_path, format="wav")