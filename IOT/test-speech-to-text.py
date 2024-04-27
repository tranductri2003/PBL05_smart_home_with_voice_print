# import speech_recognition as sr

# # Khởi tạo đối tượng Recognizer
# recognizer = sr.Recognizer()

# # Sử dụng microphone để ghi âm trong 5 giây
# with sr.Microphone() as source:
#     print("Hãy nói gì đó trong vòng 5 giây...")
#     audio_data = recognizer.record(source, duration=5)

#     try:
#         # Sử dụng Google Web Speech API để nhận dạng văn bản từ âm thanh
#         text = recognizer.recognize_google(audio_data, language="vi-VN")
#         print("Văn bản được nhận dạng: ", text)
#     except sr.UnknownValueError:
#         print("Không thể nhận dạng văn bản từ âm thanh.")
#     except sr.RequestError as e:
#         print("Lỗi trong quá trình gửi yêu cầu: ", e)
import speech_recognition as sr

# Khởi tạo đối tượng Recognizer
recognizer = sr.Recognizer()

# Mở file âm thanh
with sr.AudioFile("/home/tranductri2003/Code/PBL05_smart_home_with_voice_print_and_antifraud_ai/IOT/temp_recorded_audio/recording_raw.wav") as source:
    # Lắng nghe và nhận dạng âm thanh
    audio_data = recognizer.record(source)
    try:
        # Sử dụng Google Web Speech API để nhận dạng văn bản từ âm thanh
        text = recognizer.recognize_google(audio_data, language="vi-VN")
        print("Văn bản được nhận dạng: ", text)
    except sr.UnknownValueError:
        print("Không thể nhận dạng văn bản từ âm thanh.")
    except sr.RequestError as e:
        print("Lỗi trong quá trình gửi yêu cầu: ", e)
