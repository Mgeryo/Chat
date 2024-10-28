from fastapi import FastAPI
from app.config import settings

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from contextlib import asynccontextmanager

from app.pages.router import router as router_pages
from app.chat.router import router as router_chat
from app.users.router import router as router_users

# настраиваем redis
@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # при выключении
    
# создаем приложение fastapi
app = FastAPI(lifespan=lifespan)

# добавляем роутеры
app.include_router(router_pages)
app.include_router(router_chat)
app.include_router(router_users)

# редиректим на страницу регистрации
@app.get("/")
def redirect():
    return RedirectResponse("/pages/register") 

# подключение CORS, чтобы запросы к API могли приходить из браузера 
origins = [
    "http://localhost:8000",
    "http://localhost",
    "http://127.18.0.1:8000",
    "http://localhost:7777",
    "http://127.18.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization",
                   ],
)



    
