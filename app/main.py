# app/main.py

import os
import json
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

# Import all your modules here, in a logical order
from .api import router
from .api.auth import auth_router
from .core.adaptation import AdaptationEngine
from .core.student_bkt_manager import StudentBKTManager
from .core.user_data_manager import user_db

app = FastAPI(
    title="VisuoGeometry-Trainer API",
    description="API cho một hệ thống luyện tập hình học thích ứng.",
    version="1.0.0",
)

# Thêm middleware CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tải dữ liệu từ tệp JSON
def load_data_from_json(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Biến global
question_bank = load_data_from_json(os.path.join('data', 'question_bank.json'))
all_knowledge_components = list(set([q['knowledge_component'] for q in question_bank]))

# Thêm các biến state vào ứng dụng
app.state.question_bank = question_bank
app.state.all_knowledge_components = all_knowledge_components
app.state.adaptation_engine = AdaptationEngine(all_kcs=all_knowledge_components)
app.state.student_managers = {}

# Bao gồm các router
app.include_router(router.router, prefix="/api", tags=["API"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])