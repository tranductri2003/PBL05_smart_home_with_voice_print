import RPi.GPIO as GPIO
import time

# Thiết lập chế độ đánh số chân
GPIO.setmode(GPIO.BCM)

# Thiết lập chân GPIO11 (BCM pin 11) làm đầu ra
GPIO.setup(11, GPIO.OUT)

def gpio_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    print(f"GPIO {pin} is ON")

def gpio_off(pin):
    GPIO.output(pin, GPIO.LOW)
    print(f"GPIO {pin} is OFF")

try:
    while True:
        gpio_on(11)  # Bật GPIO11
        time.sleep(2)  # Đợi 2 giây
        gpio_off(11)  # Tắt GPIO11
        time.sleep(2)  # Đợi 2 giây

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()  # Dọn dẹp các thiết lập GPIO
