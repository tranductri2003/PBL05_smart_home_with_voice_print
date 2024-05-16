import RPi.GPIO as GPIO
import time

# Thiết lập chế độ đánh số chân
GPIO.setmode(GPIO.BCM)

# Thiết lập chân GPIO17 làm đầu ra
GPIO.setup(17, GPIO.OUT)

# Thiết lập chân GPIO27 làm đầu ra và đặt mức thấp (GND)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)

def gpio_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    print(f"GPIO {pin} is ON")

def gpio_off(pin):
    GPIO.output(pin, GPIO.LOW)
    print(f"GPIO {pin} is OFF")

try:
    while True:
        gpio_on(17)  # Bật GPIO17
        time.sleep(2)  # Đợi 2 giây
        gpio_off(17)  # Tắt GPIO17
        time.sleep(2)  # Đợi 2 giây

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()  # Dọn dẹp các thiết lập GPIO
