import RPi.GPIO as GPIO
import requests
import subprocess

class API:
    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.ip_address = self.find_ip()

        
    def find_ip(self):
        # Sử dụng lệnh arp -a để lấy danh sách các thiết bị trong mạng local và thông tin ARP của chúng
        cmd = ['arp', '-a']
        returned_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        decoded_output = returned_output.decode('utf-8')

        # Tìm kiếm địa chỉ IP dựa trên địa chỉ MAC
        lines = decoded_output.split('\n')
        for line in lines:
            if self.mac_address in line:
                ip = line.split()[1][1:-1]  # Trích xuất địa chỉ IP từ output
                return ip

    # Trả về None nếu không tìm thấy địa chỉ IP cho địa chỉ MAC đích
        return None

    def get_data(self):
        return self.data
    
    def send_data(self, data):                
        url = 'http://' + self.ip_address + ':10000/message'
        response = requests.post(url, data, timeout=10)
        
        # Kiểm tra xem yêu cầu có thành công hay không (status code 200 là thành công)
        if response.status_code == 200:
            print('Yêu cầu API thành công!')
            # Hiển thị nội dung phản hồi từ API
        else:
            print('Yêu cầu API không thành công!')
        
# data = {
#     "Garage Led": 0,
#     "Garage Door": 0,
#     "Living Led": 0,
#     "Kitchen Led": 0,
#     "Parent Led": 0,
#     "Children Led": 0,
#     "Temperature": 0,
#     "Humidity": 0,
# }

# # Sử dụng lớp API
# mac_address = "a0:a3:b3:ab:2e:10"
# api = API(mac_address)


# # Cập nhật dữ liệu
# api.send_data(data)
# api.send_data(data)
# api.send_data(data)
