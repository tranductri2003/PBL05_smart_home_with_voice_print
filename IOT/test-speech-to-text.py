import speech_recognition as sr

# Khởi tạo đối tượng Recognizer
recognizer = sr.Recognizer()

# Sử dụng microphone để ghi âm trong 5 giây
with sr.Microphone() as source:
    print("Hãy nói gì đó trong vòng 5 giây...")
    audio_data = recognizer.record(source, duration=5)

    try:
        # Sử dụng Google Web Speech API để nhận dạng văn bản từ âm thanh
        text = recognizer.recognize_google(audio_data, language="vi-VN")
        print("Văn bản được nhận dạng: ", text)
    except sr.UnknownValueError:
        print("Không thể nhận dạng văn bản từ âm thanh.")
    except sr.RequestError as e:
        print("Lỗi trong quá trình gửi yêu cầu: ", e)
