# app/main.py

import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from passlib.context import CryptContext
import secrets

# Import các router và các lớp logic từ các gói con trong cùng gói 'app'
from .api.router import router
from .api.auth import router as auth_router
from .core.adaptation import AdaptationEngine
from .core.student_bkt_manager import StudentBKTManager
from .core.user_data_manager import user_db, get_user, save_user_db
from .core.security import ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash

app = FastAPI(
    title="VisuoGeometry-Trainer",
    description="Ứng dụng giúp học sinh lớp 7 luyện tập hình học trực quan.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:8000",
    "null",                  
    "https://dqnam268-vtt.github.io",
    "https://dqnam268-vtt.github.io/VisuoGeometry-Trainer",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Ứng dụng đang khởi động...")
    
    question_bank_path = 'app/data/question_bank.json'
    try:
        with open(question_bank_path, "r", encoding="utf-8") as f:
            question_data = json.load(f)
        app.state.question_bank = question_data
        print(f"Đã tải {len(question_data)} câu hỏi từ {question_bank_path}")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{question_bank_path}'. Vui lòng đảm bảo tệp nằm đúng đường dẫn.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Lỗi: Không thể đọc tệp '{question_bank_path}'. Đảm bảo tệp là JSON hợp lệ.")
        exit(1)

    all_kcs = sorted(list(set(q["knowledge_component"] for q in question_data)))
    app.state.all_knowledge_components = all_kcs
    print(f"Đã phát hiện {len(all_kcs)} thành phần kiến thức (Knowledge Components): {', '.join(all_kcs)}")

    app.state.adaptation_engine = AdaptationEngine(all_kcs=all_kcs)
    print("Đã khởi tạo Adaptation Engine.")

    app.state.student_managers = {}
    print("Đã khởi tạo bộ quản lý học sinh (cache).")

    try:
        user_db_path = "user_data.json"
        if not os.path.exists(user_db_path):
            print("Không tìm thấy user_data.json, tạo cơ sở dữ liệu người dùng mới.")
            _initialize_user_db()
        else:
            print("Đã tìm thấy user_data.json, đang tải dữ liệu người dùng.")
            with open(user_db_path, "r", encoding="utf-8") as f:
                loaded_users = json.load(f)
                user_db.update(loaded_users)
    except Exception as e:
        print(f"Lỗi khi tải hoặc tạo cơ sở dữ liệu người dùng: {e}")
        exit(1)

    print("Ứng dụng khởi động hoàn tất.")

def _initialize_user_db():
    test_user_password = "test_password"
    hashed_password = get_password_hash(test_user_password)
    user_db["test_user"] = {
        "username": "test_user",
        "hashed_password": hashed_password
    }
    save_user_db()
    print("Đã tạo người dùng thử nghiệm: 'test_user' với mật khẩu 'test_password'")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(router, prefix="/api/v1")