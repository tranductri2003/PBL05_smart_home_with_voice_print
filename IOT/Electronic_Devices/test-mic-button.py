import RPi.GPIO as GPIO

# Thiết lập chế độ sử dụng GPIO theo BCM
GPIO.setmode(GPIO.BCM)

# Thiết lập chân GPIO2 là chân input (đầu vào từ nút nhấn)
GPIO.setup(2, GPIO.IN)

# Thiết lập chân GPIO22 là chân output (đầu ra điều khiển LED) và đặt trạng thái ban đầu là HIGH
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)

try:
    while True:
        # Đọc trạng thái của chân GPIO2
        button_state = GPIO.input(2)
        
        # Nếu nút được nhấn (trạng thái là LOW), in ra thông báo
        if button_state == GPIO.LOW:
            print("Nút đã được nhấn")
            # Bật LED (tắt nếu muốn)
            GPIO.output(22, GPIO.HIGH)
        else:
            print("Chưa nhấn nút")
            # Tắt LED (bật nếu muốn)
            GPIO.output(22, GPIO.LOW)

except KeyboardInterrupt:
    print("Thoát chương trình")

finally:
    # Dọn dẹp GPIO
    GPIO.cleanup()
