from pydub import AudioSegment
import os

# Function to split audio file into segments of specified length
def split_audio(input_file, output_folder, segment_length=1000):
    audio = AudioSegment.from_wav(input_file)
    duration = len(audio)
    for i in range(0, duration, segment_length):
        segment = audio[i:i+segment_length]
        output_file = os.path.join(output_folder, os.path.basename(input_file).replace('.wav', f'_{i//segment_length}.wav'))
        segment.export(output_file, format="wav")

# Folder containing audio files
input_folder = 'our-voices/audio'

# Loop through each subfolder
for folder in os.listdir(input_folder):
    folder_path = os.path.join(input_folder, folder)
    if os.path.isdir(folder_path):
        # Loop through each audio file in the subfolder
        for audio_file in os.listdir(folder_path):
            if audio_file.endswith('.wav'):
                input_file = os.path.join(folder_path, audio_file)
                output_folder = folder_path
                split_audio(input_file, output_folder)
