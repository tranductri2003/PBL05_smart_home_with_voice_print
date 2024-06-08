from gtts import gTTS
import pygame
import os

def speak_text(text, lang='vi', volume=1.0):
    # Sử dụng gTTS để chuyển văn bản thành giọng nói
    tts = gTTS(text=text, lang=lang, slow=False)

    # Lưu giọng nói vào một file tạm thời
    tts.save("temp.mp3")

    # Khởi tạo pygame mixer
    pygame.mixer.init()

    # Tải và phát file âm thanh
    pygame.mixer.music.load("temp.mp3")
    
    # Tăng âm lượng
    pygame.mixer.music.set_volume(volume)

    pygame.mixer.music.play()

    # Chờ cho đến khi phát xong
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Xóa file tạm
    os.remove("temp.mp3")

# Văn bản cần chuyển thành giọng nói
text_to_speak = "Xin chào mọi người. Tôi là Trần Đức Trí đây. Nhiệt độ hôm nay là 25 độ C và độ ẩm là 28 %"
# Tăng âm lượng lên 50%
speak_text(text_to_speak, volume=1)
