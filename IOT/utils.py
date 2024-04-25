import subprocess
import re

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', input_path, '-ar', str(target_sample_rate), output_path]
    subprocess.run(command, check=True)

def speech2text(wav_file, model):
    return model(wav_file)['text']

# Function to extract action and device
def extract_action_and_device(sentence):
    # Updated regular expression pattern
    pattern = r"(mở|đóng|bật|tắt)\s+(cửa cuốn nhà xe|đèn nhà xe|cửa trượt phòng khách|đèn phòng khách|cửa phòng ngủ ba mẹ|đèn phòng ngủ ba mẹ|cửa phòng ngủ con cái|đèn phòng ngủ con cái|đèn phòng bếp)\b"

    match = re.search(pattern, sentence)
    if match:
        action = match.group(1).strip()
        device = match.group(2).strip()
        return action, device
    else:
        return None, None


"""
mở cửa cuốn nhà xe
đóng cửa cuốn nhà xe
bật đèn nhà xe
tắt đèn nhà xe

mở cửa trượt phòng khách
bật đèn phòng khách
tắt đèn phòng khách

mở cửa phòng ngủ ba mẹ
bật đèn phòng ngủ ba mẹ
tắt đèn phòng ngủ ba mẹ

mở cửa phòng ngủ con cái
bật đèn phòng ngủ con cái
tắt đèn phòng ngủ con cái

bật đèn phòng bếp
tắt đèn phòng bếp
"""

