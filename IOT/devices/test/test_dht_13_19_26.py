import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# Thiết lập chế độ đánh số chân
GPIO.setmode(GPIO.BCM)

# Thiết lập chân GPIO13 làm đầu ra đặt mức cao
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)

# Thiết lập cảm biến DHT22
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 19  # Chân GPIO mà DHT22 kết nối tới

# Thiết lập chân GPIO6 làm đầu ra và đặt mức thấp (GND)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.LOW)


    

def read_dht22():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
    else:
        print("Failed to retrieve data from humidity sensor")

try:
    while True:
        
        read_dht22()
        time.sleep(2)  # Đọc dữ liệu mỗi 2 giây

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()  # Dọn dẹp các thiết lập GPIO

    """
    import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import requests
import subprocess
# Thiết lập chế độ đánh số chân
GPIO.setmode(GPIO.BCM)

# Thiết lập chân GPIO13 làm đầu ra đặt mức cao
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)

# Thiết lập cảm biến DHT22
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 19  # Chân GPIO mà DHT22 kết nối tới

# Thiết lập chân GPIO6 làm đầu ra và đặt mức thấp (GND)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.LOW)

def find_ip_by_mac(target_mac):
    # Sử dụng lệnh arp -a để lấy danh sách các thiết bị trong mạng local và thông tin ARP của chúng
    cmd = ['arp', '-a']
    returned_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    decoded_output = returned_output.decode('utf-8')

    # Tìm kiếm địa chỉ IP dựa trên địa chỉ MAC
    lines = decoded_output.split('\n')
    for line in lines:
        if target_mac in line:
            ip = line.split()[1][1:-1]  # Trích xuất địa chỉ IP từ output
            return ip

    # Trả về None nếu không tìm thấy địa chỉ IP cho địa chỉ MAC đích
    return None
# Địa chỉ MAC của ESP32 mà bạn muốn truy cập
target_mac = "a0:a3:b3:ab:2e:10"

data = {
    "Garage Led": 0,
    "Garage Door": 0,
    "Living Led": 0,
    "Kitchen Led": 0,
    "Parent Led": 0,
    "Children Led": 0,
    "Temperature": 0,
    "Humidity": 0,
}
        
# Tìm địa chỉ IP dựa trên địa chỉ MAC
ip_address = find_ip_by_mac(target_mac)
print(ip_address)




def send_api(humidity, temperature):
    
    url = 'http://' + ip_address + ':10000/message'
    
    
    data["Humidity"] = humidity
    data["Temperature"] = temperature
    response = requests.post(url, data=data, timeout=10)


    # Kiểm tra xem yêu cầu có thành công hay không (status code 200 là thành công)
    if response.status_code == 200:
        print('Yêu cầu API thành công!')
        # Hiển thị nội dung phản hồi từ API
    else:
        print('Yêu cầu API không thành công!')
    

def read_dht22():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
        if ip_address:
            send_api(humidity, temperature)
        else:
            print('Cannot find a esp32')
    else:
        print("Failed to retrieve data from humidity sensor")

try:
    while True:
        
        read_dht22()
        time.sleep(2)  # Đọc dữ liệu mỗi 2 giây

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup()  # Dọn dẹp các thiết lập GPIO

    """