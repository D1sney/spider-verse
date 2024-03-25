from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer

# авторизация
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(payload: dict):
    # header: генерируется сам и показывает что это jwt и algoritm
    # payload: то что мы передаем
    # signature: генерируется из payload и SECRET_KEY
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # exp - этот параметр отвечает за срок годности токена, в него нужно передать дату и время, а не период времени
    payload.update({'exp': expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # проверка на срок годности токена
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Signature has expired', headers={'WWW-Authenticate': 'Bearer'})
        
        # то что мы передавали в токен
        username = payload.get('username')

        if username is None:
            raise credentials_exception
        # data которая содержится в проверяемом токене, по нашей модели токена
        token_payload = schemas.TokenPayload(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_payload


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    
    token_payload = verify_access_token(token, credentials_exception)
    # по данным в payload мы находим user в нашей бд и возвращаем его
    current_user = db.query(models.User).filter(models.User.email == token_payload.username).first()
    return current_user

