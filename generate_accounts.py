import bcrypt
import random
import string
import csv

# ==========================================================
# Cấu hình
# ==========================================================
# Số lượng tài khoản bạn muốn tạo
NUM_ACCOUNTS = 50

# Độ dài của mật khẩu ngẫu nhiên
PASSWORD_LENGTH = 8

# Tên file CSV sẽ được tạo ra
CSV_FILE_PATH = "accounts_list.csv"

# ==========================================================
# Hàm hỗ trợ
# ==========================================================
def generate_random_password(length=PASSWORD_LENGTH):
    """
    Hàm sinh mật khẩu ngẫu nhiên với độ dài cho trước
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# ==========================================================
# Xử lý chính
# ==========================================================
print(f"Bắt đầu quá trình tạo {NUM_ACCOUNTS} tài khoản...")

accounts_data = []

for i in range(1, NUM_ACCOUNTS + 1):
    # Tạo tên đăng nhập theo thứ tự
    username = f"user_{i:03d}"
    
    # Tạo mật khẩu tạm thời chưa được băm
    temporary_password = generate_random_password()
    
    # Băm mật khẩu để đảm bảo an toàn khi lưu vào database
    # Bạn sẽ lưu mã băm này vào database của mình
    hashed_password = bcrypt.hashpw(temporary_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Lưu dữ liệu vào danh sách
    accounts_data.append({
        "username": username,
        "temporary_password": temporary_password, # Dùng cho file CSV
        "hashed_password": hashed_password        # Dùng cho database
    })
    
    print(f"  -> Đã tạo tài khoản {username}")

print("\nĐã hoàn tất việc tạo tài khoản và băm mật khẩu.")

# ==========================================================
# Xuất ra file CSV
# ==========================================================
print(f"\nĐang xuất danh sách tài khoản ra file '{CSV_FILE_PATH}'...")

with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['username', 'temporary_password']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    for account in accounts_data:
        writer.writerow({
            'username': account['username'],
            'temporary_password': account['temporary_password']
        })

print(f"Đã xuất file CSV thành công. Bạn có thể mở file '{CSV_FILE_PATH}' để xem.")

# ==========================================================
# LƯU Ý QUAN TRỌNG
# ==========================================================
# Sau khi chạy đoạn mã này, bạn cần lấy dữ liệu username và hashed_password
# từ biến `accounts_data` để chèn vào cơ sở dữ liệu của bạn.
# Ví dụ:
# for account in accounts_data:
#     # Thực hiện câu lệnh SQL INSERT vào database của bạn
#     # INSERT INTO users (username, password) VALUES ('{account['username']}', '{account['hashed_password']}')
#     pass