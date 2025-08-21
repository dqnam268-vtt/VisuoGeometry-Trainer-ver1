# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional

from ..schemas.user import Token, UserInDB
from ..core.security import verify_password, create_access_token
from ..core.user_data_manager import user_db

# Cấu hình
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Router
auth_router = APIRouter()

# Hàm hỗ trợ
def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = user_db.get(username)
    if not user:
        return None
    # Sửa lỗi: Sử dụng hàm verify_password để so sánh mật khẩu băm
    if not verify_password(password, user['hashed_password']):
        return None
    return user

@auth_router.post("/token", response_model=Token, tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tên người dùng hoặc mật khẩu",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}