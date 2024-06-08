import RPi.GPIO as GPIO

# Thiết lập chế độ đánh số chân (BOARD hoặc BCM)
GPIO.setmode(GPIO.BCM)  # Sử dụng hệ thống đánh số BCM

# Thiết lập các chân GPIO bạn muốn sử dụng
pins = [14, 15, 18, 23, 24]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Đặt mức thấp cho các chân này

try:
    # Thực hiện các tác vụ với GPIO nếu cần
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)  # Đặt mức cao cho các chân này
        # Bạn có thể thêm các thao tác khác ở đây
finally:
    # Chỉ dọn dẹp các chân GPIO cụ thể
    GPIO.cleanup(pins)
