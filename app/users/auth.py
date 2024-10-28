from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

from app.exceptions import IncorrectUsernameOrPassword
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# хэшируем пароль перед записью в бд
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# верифицируем пароль
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# создаем JWT токен
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

# проводим аутентификацию пользователя
async def authenticate_user(username: str, password: str):
    user = await UsersDAO.find_one_or_none(username=username)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectUsernameOrPassword
    return user