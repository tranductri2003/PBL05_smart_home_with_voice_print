import subprocess

def convert_sample_rate(input_path, output_path, target_sample_rate=16000):
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-y', '-i', input_path, '-ar', str(target_sample_rate), output_path]
    subprocess.run(command, check=True)
import re

# Updated regular expression pattern
pattern = r"(mở|đóng|bật|tắt)\s+(cửa cuốn nhà xe|đèn nhà xe|cửa trượt phòng khách|đèn phòng khách|cửa phòng ngủ ba mẹ|đèn phòng ngủ ba mẹ|cửa phòng ngủ con cái|đèn phòng ngủ con cái|đèn phòng bếp)\b"

# Function to extract action and device
def extract_action_and_device(sentence):
    match = re.search(pattern, sentence)
    if match:
        action = match.group(1).strip()
        device = match.group(2).strip()
        return action, device
    else:
        return None, None


"""
Tôi muốn mở cửa cuốn nhà xe
Tôi muốn đóng cửa cuốn nhà xe
Tôi muốn bật đèn nhà xe
Tôi muốn tắt đèn nhà xe

Tôi muốn mở cửa trượt phòng khách
Tôi muốn bật đèn phòng khách
Tôi muốn tắt đèn phòng khách

Tôi muốn mở cửa phòng ngủ ba mẹ
Tôi muốn bật đèn phòng ngủ ba mẹ
Tôi muốn tắt đèn phòng ngủ ba mẹ

Tôi muốn mở cửa phòng ngủ con cái
Tôi muốn bật đèn phòng ngủ con cái
Tôi muốn tắt đèn phòng ngủ con cái

Tôi muốn bật đèn phòng bếp
Tôi muốn tắt đèn phòng bếp
"""