# app/main.py

import os
import json
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from pathlib import Path 

# Import các module khác
from .api import router
from .api.auth import auth_router
from .core.adaptation import AdaptationEngine
from .core.student_bkt_manager import StudentBKTManager
from .core.user_data_manager import user_db

# --- CÁC THAY ĐỔI CẦN THIẾT ---
# Tạo một APIRouter chính để gộp tất cả các router con
api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(router.router, tags=["API"])
api_router.include_router(auth_router, tags=["Auth"])
# --- KẾT THÚC THAY ĐỔI ---

app = FastAPI(
    title="VisuoGeometry-Trainer API",
    description="API cho một hệ thống luyện tập hình học thích ứng.",
    version="1.0.0",
)

# Thêm cấu hình CORS để cho phép frontend truy cập backend
origins = [
    "https://dqnam268-vtt.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THAY ĐỔI LỚN: Tải dữ liệu bằng đường dẫn tuyệt đối ---
try:
    app_dir = Path(__file__).parent
    json_file_path = app_dir / "data" / "question_bank.json"

    print(f"Đang tải ngân hàng câu hỏi từ: {json_file_path}")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        question_bank = json.load(f)

except FileNotFoundError:
    print(f"LỖI NGHIÊM TRỌNG: Không tìm thấy tệp question_bank.json tại: {json_file_path}")
    raise
# --- KẾT THÚC THAY ĐỔI ---

all_knowledge_components = list(set([q['knowledge_component'] for q in question_bank]))

# Thêm các biến state vào ứng dụng
app.state.question_bank = question_bank
app.state.all_knowledge_components = all_knowledge_components
app.state.adaptation_engine = AdaptationEngine(all_kcs=all_knowledge_components)
app.state.student_managers = {}

# Thêm router chính đã được gộp vào ứng dụng
app.include_router(api_router)