import RPi.GPIO as GPIO
import time

# Thiết lập chân GPIO
ENA = 14
IN1 = 15
IN2 = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Tạo PWM cho ENA
pwm = GPIO.PWM(ENA, 10)  # 100 Hz
pwm.start(0)  # Bắt đầu với duty cycle 0%

try:
    # Điều khiển động cơ
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(10)  # Duty cycle 50%
    time.sleep(5)  # Chạy động cơ trong 5 giây
finally:
    # Dừng động cơ và làm sạch GPIO
    pwm.stop()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.cleanup()
