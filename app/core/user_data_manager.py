# app/core/user_data_manager.py

import json
import os
import bcrypt
from typing import Dict
from ..schemas.user import UserInDB
from ..core.security import get_password_hash

# Đường dẫn đến tệp dữ liệu người dùng
USERS_DB_FILE = "./user_db.json"

# Giả lập cơ sở dữ liệu người dùng
user_db: Dict[str, dict] = {}

def load_users_from_file():
    global user_db
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, "r", encoding='utf-8') as f:
            user_db = json.load(f)

def save_users_to_file():
    with open(USERS_DB_FILE, "w", encoding='utf-8') as f:
        json.dump(user_db, f, indent=4)

def get_user(username: str):
    return user_db.get(username)

def create_user(new_user: UserInDB):
    hashed_password = get_password_hash(new_user.password)
    user_data = {
        "username": new_user.username,
        "hashed_password": hashed_password
    }
    user_db[new_user.username] = user_data
    save_users_to_file()

# Tải dữ liệu người dùng khi khởi động ứng dụng
load_users_from_file()

# Nếu không có người dùng nào, tạo một số người dùng mặc định
if not user_db:
    # Mật khẩu gốc: "test_password"
    hashed_password = get_password_hash("test_password")
    user_db["test_user"] = {
        "username": "test_user",
        "hashed_password": hashed_password
    }
    
    # Mật khẩu gốc: "demo_password"
    hashed_password_demo = get_password_hash("demo_password")
    user_db["demo_user"] = {
        "username": "demo_user",
        "hashed_password": hashed_password_demo
    }

    save_users_to_file()
    print("Đã tạo người dùng mặc định: 'test_user' và 'demo_user'.")