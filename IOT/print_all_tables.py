import sqlite3

def print_tables_in_database(db_path):
    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Truy vấn để lấy tên của tất cả các bảng trong cơ sở dữ liệu
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # In ra tên của các bảng
    print("Các bảng có trong cơ sở dữ liệu:")
    for table in tables:
        print(table[0])

    # Đóng kết nối đến cơ sở dữ liệu
    conn.close()

# Gọi hàm để in ra tất cả các bảng trong cơ sở dữ liệu
print_tables_in_database("D:\Code\BachKhoa\PBL 5\PBL05_smart_home_with_voice_print_and_antifraud_ai\BackEnd\db.sqlite3")
