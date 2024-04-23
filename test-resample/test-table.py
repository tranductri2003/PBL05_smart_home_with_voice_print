from tabulate import tabulate
from colorama import Fore, Back, Style
import math

class DeviceTextDisplay:
    def __init__(self, devices,n_columns, title="My Smart Home"):
        self.devices = devices
        self.title = title
        self.n_columns = n_columns

    def display(self):
        # Định dạng danh sách các thiết bị thành bảng
        headers = [self.title.center(30)] * self.n_columns  # Tạo tiêu đề cho mỗi cột
        table = []
        for i in range(0, len(self.devices), self.n_columns):
            # Thêm các thiết bị vào bảng theo hàng, mỗi hàng tối đa 3 thiết bị
            row = [self.devices[i+j] if i+j < len(self.devices) else "" for j in range(self.n_columns)]
            # Thay đổi màu sắc của các hàng
            if (i/self.n_columns) % 2 == 0:
                rowa = []
                for device in row:
                    if 'Đèn' in device:
                        rowa.append(Back.BLUE + device + '💡'+ ': _' + Style.RESET_ALL)
                    elif 'Cửa' in device:
                        rowa.append(Back.BLUE + device + '🚪'+ ': _' + Style.RESET_ALL)
                    else:
                        rowa.append("")

            elif (i/self.n_columns) % 2 == 1:
                rowa = []
                for device in row:
                    if 'Đèn' in device:
                        rowa.append(Back.YELLOW + device + '💡'+ ': _' + Style.RESET_ALL)
                    elif 'Cửa' in device:
                        rowa.append(Back.YELLOW + device + '🚪'+ ': _' + Style.RESET_ALL)
                    else:
                        rowa.append("")
            table.append(rowa)

        # In bảng với đường viền
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

# Danh sách các thiết bị
devices = [
    "Đèn garage",
    "Cửa cuốn garage",
    "Cửa trượt phòng khách",
    "Đèn phòng khách",
    "Cửa phòng ngủ ba mẹ",
    "Đèn phòng ngủ ba mẹ",
    "Cửa phòng ngủ con cái",
    "Đèn phòng ngủ con cái",
    "Đèn phòng bếp"
]

n_columns = int(input("Nhập số cột: "))




# Tạo instance của class và hiển thị
device_display = DeviceTextDisplay(devices, n_columns)
device_display.display()