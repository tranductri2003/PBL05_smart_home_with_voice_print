import RPi.GPIO as GPIO
import time

buttonPin = 22    # Chân nhận tín hiệu của nút nhấn
  # Chân cấp nguồn cho đèn LED

GPIO.setmode(GPIO.BCM)  # Đặt chế độ chân GPIO là BOARDz

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Thiết lập chân nút nhấn là đầu vào với điện trở pull-up
                            # Thiết lập chân đèn LED là đầu ra
try:
    while True:
        # Đọc trạng thái của nút nhấn
        buttonState = GPIO.input(buttonPin)
        
        # Nếu nút được nhấn (trạng thái là LOW), in ra thông báo và bật đèn LED
        if buttonState == GPIO.LOW:
            print("Nút đã được nhấn")
        # Nếu nút không được nhấn, in ra thông báo và tắt đèn LED
        else:
            print("Chưa nhấn nút")
        
        time.sleep(1)  # Đợi một chút để tránh đọc nút quá nhanh

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # Dọn dẹp GPIO khi kết thúc chương trình
