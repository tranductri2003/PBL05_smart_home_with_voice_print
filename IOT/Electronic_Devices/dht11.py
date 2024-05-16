import RPi.GPIO as GPIO
import time
import Adafruit_DHT

class DHTSensor:
    def __init__(self, high_pin, data_pin, low_pin):
        self.high_pin = high_pin
        self.data_pin = data_pin
        self.low_pin = low_pin

        # Thiết lập chế độ đánh số chân
        GPIO.setmode(GPIO.BCM)

        # Thiết lập chân GPIO làm đầu ra và đặt mức cao
        GPIO.setup(self.high_pin, GPIO.OUT)
        GPIO.output(self.high_pin, GPIO.HIGH)

        # Thiết lập chân GPIO làm đầu ra và đặt mức thấp (GND)
        GPIO.setup(self.low_pin, GPIO.OUT)
        GPIO.output(self.low_pin, GPIO.LOW)

    def read_dht11(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.data_pin)
        if humidity is None: 
            humidity = 0
        if temperature is None:
            temperature = 0
        # if humidity is not None and temperature is not None:
        #     print(f"Temperature: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
        # else:
        #     print("Failed to retrieve data from humidity sensor")
        return humidity, temperature
    
    def cleanup(self):
        GPIO.cleanup()

# # Sử dụng lớp DHTSensor với các tham số tùy chỉnh
# try:
#     dht_sensor = DHTSensor(13, 19, 26)  # Chân HIGH là 13, chân DATA là 19, chân LOW là 26
#     while True:
#         print(dht_sensor.read_dht11())
#         time.sleep(2)  # Đọc dữ liệu mỗi 2 giây

# except KeyboardInterrupt:
#     print("Program terminated")

# finally:
#     dht_sensor.cleanup()  # Dọn dẹp các thiết lập GPIO
