# app/core/user_data_manager.py

import json
import os
from typing import Dict

user_db: Dict = {}
USER_DB_FILE = "user_data.json"

def get_user(username: str):
    """Lấy thông tin người dùng từ cơ sở dữ liệu giả."""
    return user_db.get(username)

def save_user_db():
    """Lưu dữ liệu người dùng vào file."""
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(user_db, f, indent=4)