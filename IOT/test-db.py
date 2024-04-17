import sqlite3

def connect_db(db_path):
    """ Tạo kết nối đến cơ sở dữ liệu SQLite được chỉ định bởi db_path """
    conn = sqlite3.connect(db_path)
    return conn

def query_data(conn):
    """ Thực hiện truy vấn dữ liệu và in kết quả """
    cursor = conn.cursor()

    # Truy vấn dữ liệu từ bảng Member
    cursor.execute("SELECT * FROM members_member")
    members = cursor.fetchall()
    print("Members:")
    for member in members:
        print(f"ID: {member[0]}, Name: {member[1]}, About: {member[2]}")

    # Truy vấn dữ liệu từ bảng Appliance
    cursor.execute("SELECT * FROM appliances_appliance")
    appliances = cursor.fetchall()
    print("\nAppliances:")
    for appliance in appliances:
        print(f"ID: {appliance[0]}, Name: {appliance[1]}, Description: {appliance[2]}")

    # Truy vấn dữ liệu từ bảng Permission
    cursor.execute("SELECT * FROM permissions_permission")
    permissions = cursor.fetchall()
    print("\nPermissions:")
    for permission in permissions:
        print(f"ID: {permission[0]}, Member ID: {permission[1]}, Appliance ID: {permission[2]}")

def main():
    db_path = 'D:\\Code\\BachKhoa\\PBL 5\\PBL05_smart_home_with_voice_print_and_antifraud_ai\\BackEnd\\db.sqlite3'
    conn = connect_db(db_path)
    try:
        query_data(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
