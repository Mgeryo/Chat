from fastapi import APIRouter, HTTPException, Response, status
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.schemas import New_user, User
from app.exceptions import UserAlreadyExistsException
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

users = []

# получем объект класса New_user, отправленного в коде javascript
@router.post("/register")
async def reg_new_user(user_data: New_user):
    # проверяем есть ли пользователь в бд
    existing_user = await UsersDAO.find_one_or_none(username = user_data.username)
    if existing_user:
        print("пользователь уже существует")
        raise UserAlreadyExistsException
        
    # хэшируем пароль и добавляем в пользователя в бд
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(username = user_data.username, hashed_password = hashed_password)
    
# получаем объект класса User    
@router.post("/login")
async def login_user(response: Response, user_data: User):
    # проводим аутентификацию
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # создаем токен
    access_token = create_access_token({"sub": str(user.id)})
    # сетим куку
    response.set_cookie("chat_access_token", access_token, httponly=True)
    
    