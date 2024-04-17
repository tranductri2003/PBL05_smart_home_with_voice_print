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
    def __init__(self, id, member_id, appliance_id):
        self.id = id
        self.member_id = member_id
        self.appliance_id = appliance_id

    def __str__(self):
        return f"Permission(ID: {self.id}, Member ID: {self.member_id}, Appliance ID: {self.appliance_id})"
    
    
    
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
    
    # Truy vấn dữ liệu từ bảng Permission và tạo các đối tượng Permission
    cursor.execute("SELECT * FROM permissions_permission")
    permissions = [Permission(*row) for row in cursor.fetchall()]
    return permissions