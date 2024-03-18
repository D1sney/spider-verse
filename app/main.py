from fastapi import FastAPI, Request, Depends, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqladmin import Admin
from . import models, schemas
from .database import engine, get_db
from admin import views

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title = 'Spider-verse'
)

# важно назвать не templates и не statics, чтобы не было конфликтов имен с sqladmin
template = Jinja2Templates(directory="template")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# Админка
admin = Admin(app, engine)
admin.add_view(views.UserAdmin)
admin.add_view(views.ArticleAdmin)


@app.get('/')
async def get_main_page(request: Request, db: Session = Depends(get_db)):
    return template.TemplateResponse("index.html", {"request": request})


@app.get('/articles', response_model=list[schemas.ArticleResponse]) # list с маленькой буквы потому что после Python 3.9 так можно делать, а в ранних версиях необходимо было импортировать List из typing
async def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all() # тут объект сессии обращается к нашим моделям и с помощью all вытягивает все значения, но после обращения к моделям можно также и менять данные в бд, а не только вытащить
    return articles

# response_model позволяет вернуть ответ пользователю в соответствии с нашей pydsntic моделью
@app.post('/articles', status_code=status.HTTP_201_CREATED, response_model=schemas.ArticleResponse)
async def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    new_article = models.Article(**article.dict()) # вариант если очень много полей и вариант ниже становится затруднительным
    # new_article = models.Article(title=article.title, full_text=article.full_text, summary=article.summary)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@app.get('/articles/{id}', status_code=200, response_model=schemas.ArticleResponse)
async def get_one_article(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()
    return article


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


@app.put('/articles/{id}', response_model=schemas.ArticleResponse)
async def update_post(id: int, updated_article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id)

    if article.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    up = updated_article.dict()
    up.pop('pubdate')
    article.update(up, synchronize_session=False)
    db.commit()
    return article.first()
