# app/api/router.py

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import StreamingResponse
import io
import pandas as pd
import random
from typing import Dict, List

from ..schemas.question import QuestionPublic, Submission, SubmissionResult, Option, Content
from ..core.adaptation import AdaptationEngine
from ..core.student_bkt_manager import StudentBKTManager
from ..core.security import get_current_user
from ..core.user_data_manager import user_db

router = APIRouter()

def get_question_bank(request: Request) -> list:
    return request.app.state.question_bank

def get_adaptation_engine(request: Request) -> AdaptationEngine:
    return request.app.state.adaptation_engine

def get_student_manager(student_id: str, request: Request) -> StudentBKTManager:
    student_managers: Dict[str, StudentBKTManager] = request.app.state.student_managers
    if student_id not in student_managers:
        all_kcs = request.app.state.all_knowledge_components
        student_managers[student_id] = StudentBKTManager(student_id=student_id, all_kcs=all_kcs)
    return student_managers[student_id]

@router.get("/session/next-question", response_model=QuestionPublic, tags=["Session"])
def get_next_question(
    request: Request, # Vị trí đúng
    current_user: str = Depends(get_current_user),
    question_bank: list = Depends(get_question_bank),
    adaptation_engine: AdaptationEngine = Depends(get_adaptation_engine),
):
    student_manager = get_student_manager(student_id=current_user, request=request)
    next_kc, next_difficulty = adaptation_engine.get_next_question_spec(student_manager=student_manager)
    
    # Giữ nguyên phần còn lại của hàm
    ...

@router.post("/session/submit-answer", response_model=SubmissionResult, tags=["Session"])
def submit_answer(
    request: Request, # Vị trí đúng
    submission: Submission,
    current_user: str = Depends(get_current_user),
    question_bank: list = Depends(get_question_bank),
):
    student_manager = get_student_manager(student_id=current_user, request=request)
    # Giữ nguyên phần còn lại của hàm
    ...

@router.get("/students/export", tags=["Students"])
def export_student_data(
    request: Request, # Vị trí đúng
    current_user: str = Depends(get_current_user),
):
    student_manager = get_student_manager(student_id=current_user, request=request)
    # Giữ nguyên phần còn lại của hàm
    ...
    
@router.get("/students/dashboard", tags=["Students"], response_model=List[Dict])
def get_dashboard_data(
    request: Request, # Vị trí đúng
    current_user: str = Depends(get_current_user),
):
    student_manager = get_student_manager(student_id=current_user, request=request)
    # Giữ nguyên phần còn lại của hàm
    ...

@router.get("/students/progress")
async def get_student_progress(
    request: Request, # Vị trí đúng
    current_user: str = Depends(get_current_user),
):
    student_manager = get_student_manager(student_id=current_user, request=request)
    # Giữ nguyên phần còn lại của hàm
    ...