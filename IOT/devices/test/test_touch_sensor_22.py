import RPi.GPIO as GPIO
import time

# Thiết lập chế độ đánh số chân GPIO
GPIO.setmode(GPIO.BCM)

# Đặt chân GPIO 22 làm đầu vào và bật lên điện trở pull-up
touch_sensor_pin = 22
GPIO.setup(touch_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Đọc trạng thái của cảm biến chạm
        if GPIO.input(touch_sensor_pin) == GPIO.HIGH:
            print("Cảm biến chạm đã được chạm")
        else:
            print("Cảm biến chạm không được chạm")
        
        # Chờ 0.1 giây trước khi đọc lại
        time.sleep(0.1)

except KeyboardInterrupt:
    # Dọn dẹp GPIO khi kết thúc chương trình
    GPIO.cleanup()
