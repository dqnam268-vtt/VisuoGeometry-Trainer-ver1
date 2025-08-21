from passlib.context import CryptContext

# Đối tượng để xử lý việc băm và kiểm tra mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Kiểm tra mật khẩu thường với mật khẩu đã băm."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Băm mật khẩu."""
    return pwd_context.hash(password)