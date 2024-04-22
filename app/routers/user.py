from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/users',
    # добавляет заголовок в документации для эндпоинтов этого роутера
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)): # Depends(oauth2.oauth2_scheme) - такой параметр токен нужно передавать для эндопоинтов в которых необходима авторизация, он проверяет наличие токена, но не проверяет сам токен на валидность
    
    # hash the password - user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/me', status_code=200)
async def get_me(current_user: str = Depends(oauth2.get_current_user)): # мы установим зависимость от oauth2_scheme в зависимотсях уровнем ниже
    # в зависимостях уже пройдены все проверки поэтому мы можем смело просто вернуть значение
    return current_user


@router.get('/{id}', status_code=200, response_model=schemas.UserResponse)
async def get_one_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    return user

