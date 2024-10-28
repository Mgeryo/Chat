from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import JSON, Column, Integer, String
from app.database import Base

class Messages(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str]

    # сериализация объекта алхимии - при обращении получаем dict, который можно конвертировать в JSON
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}