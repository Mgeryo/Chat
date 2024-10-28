
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import JSON, Column, Integer, String
from app.database import Base

    
class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    
    