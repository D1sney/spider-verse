from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # schemas.UserLogin - моя модель, при которой надо вручнуй вводить json в документации
    # OAuth2PasswordRequestForm = Depends() - это встроенная модель в FasAPI, которая не работает без Depends()
    # Depends() - Используется для создания зависимости, при ней передаются аргументы и отображаются в документации в виде параметров,
    # даже если до этого они должны были быть в теле запроса, Depends() вызывает переданную в нее функцию с переданными в нее новыми параметрами
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    # create token
    # return token
    access_token = oauth2.create_access_token({'username': user_credentials.username})
    return {'access_token': access_token, 'token_type': 'bearer'}
