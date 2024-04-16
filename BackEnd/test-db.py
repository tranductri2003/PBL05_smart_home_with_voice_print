import os
import django

# Thiết lập biến môi trường DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Thiết lập môi trường Django
django.setup()

# Import các mô hình từ ứng dụng của bạn
from members.models import Member
from appliances.models import Appliance
from permissions.models import Permission

# Truy xuất thông tin từ cơ sở dữ liệu
def get_information():
    # Lấy tất cả các thành viên
    all_members = Member.objects.all()
    print("Members:")
    for member in all_members:
        print(f"ID: {member.id}, Name: {member.name}, About: {member.about}")

    # Lấy tất cả các thiết bị
    all_appliances = Appliance.objects.all()
    print("\nAppliances:")
    for appliance in all_appliances:
        print(f"ID: {appliance.id}, Name: {appliance.name}, Description: {appliance.description}")

    # Lấy tất cả các quyền
    all_permissions = Permission.objects.all()
    print("\nPermissions:")
    for permission in all_permissions:
        print(f"ID: {permission.id}, Name: {permission.member.name}, Description: {permission.appliance.name}")

# Gọi hàm để hiển thị thông tin
get_information()
