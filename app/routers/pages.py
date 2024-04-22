from fastapi import status, HTTPException, Request, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import main, models, schemas, oauth2
from ..database import get_db
from . import article


router = APIRouter(
    prefix='/pages',
    # добавляет заголовок в документации для эндпоинтов этого роутера
    tags=['Pages']
)


@router.get('/base')
async def get_base_page(request: Request):
    return main.template.TemplateResponse("base.html", {"request": request})

# @router.get('/home')
# async def get_home_page(request: Request, operations = Depends(article.get_articles)): # эта зависимость неподходит потому что обращается к защищеному эндпоинту, а мы к нему обратимся уже внутри js кода
#     # важно передать в jinja operations
#     return main.template.TemplateResponse("home.html", {"request": request, "operations": operations}) # operations используются в jinja

@router.get('/home')
async def get_home_page(request: Request): # эта зависимость неподходит потому что обращается к защищеному эндпоинту, а мы к нему обратимся уже внутри js кода
    # важно передать в jinja operations
    return main.template.TemplateResponse("home.html", {"request": request}) # operations используются в jinja