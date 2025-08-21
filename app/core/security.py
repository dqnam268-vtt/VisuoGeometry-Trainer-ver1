# app/core/security.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Import các hàm cần thiết từ các file khác
from .user_data_manager import get_user
from .hashing import verify_password # <<< THAY ĐỔI QUAN TRỌNG

# Các tham số cấu hình bảo mật
SECRET_KEY = "your-secret-key"  # Thay thế bằng một chuỗi ngẫu nhiên mạnh
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")

# --- Phần mã xử lý mật khẩu (pwd_context, get_password_hash) đã được XÓA ---
# --- Hàm verify_password gốc cũng đã được XÓA và giờ được import từ hashing.py ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Tạo JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Lấy người dùng hiện tại từ JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user["username"]