import sqlite3

class Member:
    def __init__(self, id, name, about):
        self.id = id
        self.name = name
        self.about = about

    def __str__(self):
        return f"Member(ID: {self.id}, Name: {self.name}, About: {self.about})"

class Appliance:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return f"Appliance(ID: {self.id}, Name: {self.name}, Description: {self.description})"

class Permission:
    def __init__(self, id, member_id, appliance_id, member_name=None, appliance_name=None):
        self.id = id
        self.member_id = member_id
        self.appliance_id = appliance_id
        self.member_name = member_name
        self.appliance_name = appliance_name

    def __str__(self):
        return f"Permission(ID: {self.id}, Member: {self.member_name}, Appliance: {self.appliance_name})"

    
def connect_db(db_path):
    """ Tạo kết nối đến cơ sở dữ liệu SQLite được chỉ định bởi db_path """
    conn = sqlite3.connect(db_path)
    return conn

def query_members(conn):
    cursor = conn.cursor()

    # Truy vấn dữ liệu từ bảng Member và tạo các đối tượng Member
    cursor.execute("SELECT * FROM members_member")
    members = [Member(*row) for row in cursor.fetchall()]
    return members

def query_appliances(conn):
    cursor = conn.cursor()

    # Truy vấn dữ liệu từ bảng Appliance và tạo các đối tượng Appliance
    cursor.execute("SELECT * FROM appliances_appliance")
    appliances = [Appliance(*row) for row in cursor.fetchall()]
    return appliances

def query_permissions(conn):
    cursor = conn.cursor()

    # Truy vấn liên kết ba bảng để lấy thông tin cần thiết
    cursor.execute("""
    SELECT p.id, p.member_id, p.appliance_id, m.name as member_name, a.name as appliance_name
    FROM permissions_permission p
    JOIN members_member m ON p.member_id = m.id
    JOIN appliances_appliance a ON p.appliance_id = a.id
    """)
    
    permissions = [Permission(*row) for row in cursor.fetchall()]
    return permissions

def query_member_files(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT mf.member_id, mf.file, mf.features, mm.name
    FROM members_memberfile mf
    JOIN members_member mm ON mf.member_id = mm.id
    """)
    member_files = [{
        'member_id': row[0],
        'file_path': row[1],
        'features': row[2],
        'member_name': row[3]
    } for row in cursor.fetchall()]
    return member_files


conn = connect_db("D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\BackEnd\db.sqlite3")
appliances = query_appliances(conn)
permissions = query_permissions(conn)
members = query_members(conn)

print("Danh sách các thành viên trong nhà:")
for member in members:
    print(member.name)

print("Danh sách các thiết bị trong nhà:")
for appliance in appliances:
    print(appliance.name)

print("Danh sách các quyền điều khiển:")
for permission in permissions:
    print(f"{permission.member_name} có quyền điều khiển {permission.appliance_name}")
    
member_files = query_member_files(conn)
print("Danh sách các vector của thành viên:")
for file in member_files:
    print(f"Member: {file['member_name']} - File: {file['file_path']} - Features: {file['features']}")