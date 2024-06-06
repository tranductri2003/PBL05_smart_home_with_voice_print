import RPi.GPIO as GPIO
import time

class TouchSensor:
    def __init__(self, pin):
        self.pin = pin
        # Thiết lập chế độ đánh số chân GPIO
        GPIO.setmode(GPIO.BCM)
        # Đặt chân GPIO làm đầu vào và bật lên điện trở pull-up
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_touched(self):
        # Đọc trạng thái của cảm biến chạm
        return GPIO.input(self.pin) == GPIO.HIGH

    def cleanup(self):
        # Dọn dẹp GPIO
        GPIO.cleanup()

# # Ví dụ sử dụng class TouchSensor
# if __name__ == "__main__":
#     touch_sensor_pin = 22
#     touch_sensor = TouchSensor(touch_sensor_pin)

#     try:
#         while True:
#             if touch_sensor.is_touched():
#                 print("Cảm biến chạm đã được chạm")
#             else:
#                 print("Cảm biến chạm không được chạm")
#             # Chờ 0.1 giây trước khi đọc lại
#             time.sleep(0.1)

#     except KeyboardInterrupt:
#         print("Kết thúc chương trình.")
#     finally:
#         touch_sensor.cleanup()
