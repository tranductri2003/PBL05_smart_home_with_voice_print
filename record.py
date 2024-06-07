import pyaudio
import wave
import time
import os
import signal
from pydub import AudioSegment
from threading import Thread

# Thiết lập các tham số ghi âm
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 300  # 5 phút
RAW_FILENAME = "DAT_5_MINUTES_recording_raw.wav"
RESAMPLED_FILENAME = "DAT_5_MINUTES_recording_resampled.wav"

# Khởi tạo PyAudio
audio = pyaudio.PyAudio()

frames = []

def signal_handler(sig, frame):
    print("\nRecording stopped.")
    save_and_convert_audio()
    os._exit(0)

def get_unique_filename(filename):
    """Tạo tên tệp duy nhất nếu tệp đã tồn tại."""
    if not os.path.exists(filename):
        return filename

    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}_copy{counter}{ext}"
    while os.path.exists(new_filename):
        counter += 1
        new_filename = f"{base}_copy{counter}{ext}"
    return new_filename

def save_and_convert_audio():
    raw_filename = get_unique_filename(RAW_FILENAME)
    resampled_filename = get_unique_filename(RESAMPLED_FILENAME)
    
    # Lưu âm thanh vào file WAV
    with wave.open(raw_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Chuyển đổi tần số lấy mẫu về 16000 Hz
    convert_sample_rate(raw_filename, resampled_filename, 16000)
    print(f"Saved raw audio to {raw_filename}")
    print(f"Saved and resampled audio to {resampled_filename}")

def convert_sample_rate(input_filename, output_filename, target_sample_rate):
    sound = AudioSegment.from_file(input_filename)
    sound = sound.set_frame_rate(target_sample_rate)
    sound.export(output_filename, format="wav")

def record_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    start_time = time.time()
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        elapsed_time = time.time() - start_time
        print(f"Recording time: {elapsed_time:.2f} seconds", end="\r")
        if elapsed_time > RECORD_SECONDS:
            break

    # Dừng ghi âm
    stream.stop_stream()
    stream.close()
    print("\nFinished recording.")
    save_and_convert_audio()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    record_thread = Thread(target=record_audio)
    record_thread.start()
    record_thread.join()

    # Dọn dẹp PyAudio
    audio.terminate()
