from fastapi import HTTPException, status

class Exception(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
        
class IncorrectUsernameOrPassword(Exception):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверное имя пользователя или пароль"
    
class TokenExpiredException(Exception):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Срок действия токена истек"
        
class TokenAbsentException(Exception):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"
        
class IncorrectTokenFormatException(Exception):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"
        
class UserIsNotPresentException(Exception):
    status_code=status.HTTP_401_UNAUTHORIZED
    
class UserAlreadyExistsException(Exception):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"