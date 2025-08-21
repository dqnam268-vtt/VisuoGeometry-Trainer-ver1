# app/core/user_data_manager.py

import json
import os
import csv
from typing import Dict
from ..schemas.user import UserInDB
# THAY ĐỔI QUAN TRỌNG: Import từ hashing.py ở đầu file
from .hashing import get_password_hash

# Đường dẫn đến tệp dữ liệu người dùng
# Lưu ý: Sửa lại đường dẫn tuyệt đối cho phù hợp với môi trường của bạn hoặc dùng đường dẫn tương đối
USERS_DB_FILE = "user_db.json"
ACCOUNTS_CSV_FILE = "accounts_list.csv"

# Giả lập cơ sở dữ liệu người dùng
user_db: Dict[str, dict] = {}

def load_users_from_file():
    global user_db
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, "r", encoding='utf-8') as f:
            user_db = json.load(f)

    if os.path.exists(ACCOUNTS_CSV_FILE):
        with open(ACCOUNTS_CSV_FILE, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                username = row['username']
                password = row['password']
                hashed_password = get_password_hash(password) # Sử dụng hàm đã import
                user_db[username] = {
                    "username": username,
                    "hashed_password": hashed_password
                }
        print(f"Đã tải {len(user_db)} tài khoản từ cả file JSON và CSV.")

def save_users_to_file():
    with open(USERS_DB_FILE, "w", encoding='utf-8') as f:
        json.dump(user_db, f, indent=4)

def get_user(username: str):
    return user_db.get(username)

def create_user(new_user: UserInDB):
    hashed_password = get_password_hash(new_user.password) # Sử dụng hàm đã import
    user_data = {
        "username": new_user.username,
        "hashed_password": hashed_password
    }
    user_db[new_user.username] = user_data
    save_users_to_file()

# Tải người dùng khi khởi động
load_users_from_file()

# Tạo người dùng mặc định nếu DB trống
if not user_db:
    hashed_password = get_password_hash("test_password")
    user_db["test_user"] = {
        "username": "test_user",
        "hashed_password": hashed_password
    }
    
    hashed_password_demo = get_password_hash("demo_password")
    user_db["demo_user"] = {
        "username": "demo_user",
        "hashed_password": hashed_password_demo
    }

    save_users_to_file()
    print("Đã tạo người dùng mặc định: 'test_user' và 'demo_user'.")