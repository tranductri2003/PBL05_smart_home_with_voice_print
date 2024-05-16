import RPi.GPIO as GPIO
import time

# Thiết lập chế độ đánh số chân
GPIO.setmode(GPIO.BCM)

# Thiết lập chân GPIO4 (BCM pin 4) làm đầu ra
GPIO.setup(4, GPIO.OUT)

def gpio_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    print(f"GPIO {pin} is ON")

def gpio_off(pin):
    GPIO.output(pin, GPIO.LOW)
    print(f"GPIO {pin} is OFF")

try:
    while True:
        gpio_on(4)  # Bật GPIO4
        time.sleep(2)  # Đợi 2 giây
        gpio_off(4)  # Tắt GPIO4
        time.sleep(2)  # Đợi 2 giây

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()  # Dọn dẹp các thiết lập GPIO
