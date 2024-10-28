
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.users.dependencies import get_current_user
from app.users.models import Users



# используем джинджу
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

# отрисовываем страницу регистрации
@router.get("/register")
def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# отрисовываем страницу логина
@router.get("/login")
def login_user(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# отрисовываем страницу чата
@router.get("/chat")
def get_chat_page(request: Request): 
    return templates.TemplateResponse("chat.html", {"request": request})