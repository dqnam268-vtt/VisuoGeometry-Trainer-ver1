# app/core/user_data_manager.py

import json
import os
from typing import Dict

user_db: Dict = {}
USER_DB_FILE = "user_data.json"

def get_user(username: str):
    return user_db.get(username)

def save_user_db():
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(user_db, f, indent=4)