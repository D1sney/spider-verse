from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import datetime
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


# модели pydantic
class User(BaseModel):
    id: int
    username: str
    hero: str
    email: str
    password: str

class Article(BaseModel):
    id: int
    title: str
    full_text: str
    summary: str
    category: str | None = None
    pubdate: datetime.datetime | None = None
    is_published: bool = True
    # "id": "int",
    # "title": "str",
    # "full_text": "str",
    # "summary": "str",
    # "category": "str | None = None",
    # "pubdate": "datetime.datetime",
    # "is_published": "bool = True"


app = FastAPI(
    title = 'Spider-verse'
)
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get('/')
async def get_main_page(request: Request, db: Session = Depends(get_db)):
    # articles имеет очень много методов по которым к нему можно обращаться
    # articles = db.query(models.Article)
    # print(dir(db))
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/articles')
async def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all() # тут объект сессии обращается к нашим моделям и с помощью all вытягивает все значения, но после обращения к моделям можно также и менять данные в бд, а не только вытащить
    return {'articles': articles}


@app.post('/articles')
async def create_article(article: Article, db: Session = Depends(get_db)):
    # сначала проходится фильтрация по pydantic моделе, потом ВЫБРАННЫЕ поля сохраняются в переменную
    # эти поля сохраняются в бд и там дополнительно могут присвоиться значения по умолчанию определенным полян
    # далее с помощью refresh возвращает немного возможно измененый этим путем объект, такой каким он сохранился в бд
    new_article = models.Article(**article.dict()) # вариант если очень много полей и вариант ниже становится затруднительным
    # new_article = models.Article(title=article.title, full_text=article.full_text, summary=article.summary)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return {'message': new_article}


@app.get('/articles/{id}', status_code=200)
async def get_one_article(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()
    return {'article': article}


# при status_code 204 нельзя вернуть json
@app.delete('/articles/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id)
    
    if article.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    article.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/articles/{id}')
async def update_post(id: int, updated_article: Article, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id)

    if article.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    # в таком случает в pydantic существует pubdate, но мы его предварительно удаляем и обновляем бд уже без pubdate
    # но более локаничным решением я считаю просто не добавлять pubdate в pydantic модель, если все равно бд всегда генерирует время
    up = updated_article.dict()
    up.pop('pubdate')
    article.update(up, synchronize_session=False)
    db.commit()
    return {'article': article.first()}
