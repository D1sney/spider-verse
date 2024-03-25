from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import database, models, utils, oauth2
from fastapi.security import OAuth2PasswordBearer


# Везде где мы возвращаем True, нам открывается админка
# А где мы возвращаем False, нас перенаправляет на страницу входа в админку
# Вместо каждой ошибки можно возвращать False чтобы нас перебрасывало на страницу входа в админку, но пока оставим сообщения об ошибках

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        # form создает поле для ввода на html странице
        username, password = form["username"], form["password"]
        
        db = database.SessionLocal()
        user = db.query(models.User).filter(models.User.email == username).first()
        db.close()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Invalid Credentials")
        if not utils.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Invalid Credentials")
        # здесь в будущем можно будет добавить проверку что у пользователя есть role Admin
        access_token = oauth2.create_access_token({'username': username})
        # сохранение сессии в куки
        request.session.update({"token": access_token})
        return True



    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True



    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        # token = OAuth2PasswordBearer(tokenUrl='login')
        if not token:
            return False
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
        token_payload = oauth2.verify_access_token(token, credentials_exception)
        # по данным в payload мы находим user в нашей бд, сейчас в этом нет необходимости, но в будущем это можно будет использовать
        db = database.SessionLocal()
        current_user = db.query(models.User).filter(models.User.email == token_payload.username).first()
        db.close()

        return True


authentication_backend = AdminAuth(secret_key="...")