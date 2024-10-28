from pydantic import BaseModel

class New_user(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    password: str    