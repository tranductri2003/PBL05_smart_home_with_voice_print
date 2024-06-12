import RPi.GPIO as GPIO
import time

class Led:
    def __init__(self, signal_pin, ground_pin=None):
        self.signal_pin = signal_pin
        self.ground_pin = ground_pin

        # Thiết lập chế độ đánh số chân
        GPIO.setmode(GPIO.BCM)

        # Thiết lập chân GPIO làm đầu ra
        GPIO.setup(self.signal_pin, GPIO.OUT)

        # Nếu chỉ có một tham số được truyền vào, không cần xử lý chân GND
        if self.ground_pin is not None:
            GPIO.setup(self.ground_pin, GPIO.OUT)
            GPIO.output(self.ground_pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.signal_pin, GPIO.HIGH)
        print(f"GPIO {self.signal_pin} is ON")

    def off(self):
        GPIO.output(self.signal_pin, GPIO.LOW)
        print(f"GPIO {self.signal_pin} is OFF")

    def blink(self, duration=2):
        self.on()
        time.sleep(duration)
        self.off()
        time.sleep(duration)

    def cleanup(self):
        GPIO.cleanup()

# # Sử dụng lớp Led
# try:

#     led_living = Led(4)
#     led_kitchen = Led(17, 27)
#     led_children = Led(10, 9)
#     led_parent = Led(11)
#     led_garage = Led(5, 6)
    
    
#     while True:
#         led_living.blink()  # Bật và tắt LED
#         led_kitchen.blink()  # Bật và tắt LED
#         led_children.blink()  # Bật và tắt LED
#         led_parent.blink()  # Bật và tắt LED
#         led_garage.blink()  # Bật và tắt LED

# except KeyboardInterrupt:
#     print("Program terminated")
# finally:
#     led_living.cleanup()  # Dọn dẹp các thiết lập GPIO
#     led_kitchen.cleanup()  # Dọn dẹp các thiết lập GPIO
#     led_children.cleanup()  # Dọn dẹp các thiết lập GPIO
#     led_parent.cleanup()  # Dọn dẹp các thiết lập GPIO
#     led_garage.cleanup()  # Dọn dẹp các thiết lập GPIO
