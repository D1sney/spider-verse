from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix='/articles',
    # добавляет заголовок в документации для эндпоинтов этого роутера
    tags=['Articles']
)


@router.get('/', response_model=list[schemas.ArticleResponse]) # list с маленькой буквы потому что после Python 3.9 так можно делать, а в ранних версиях необходимо было импортировать List из typing
async def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all() # тут объект сессии обращается к нашим моделям и с помощью all вытягивает все значения, но после обращения к моделям можно также и менять данные в бд, а не только вытащить
    return articles

# response_model позволяет вернуть ответ пользователю в соответствии с нашей pydsntic моделью
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ArticleResponse)
async def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    new_article = models.Article(**article.dict()) # вариант если очень много полей и вариант ниже становится затруднительным
    # new_article = models.Article(title=article.title, full_text=article.full_text, summary=article.summary)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@router.get('/{id}', status_code=200, response_model=schemas.ArticleResponse)
async def get_one_article(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()
    return article


# при status_code 204 нельзя вернуть json
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id)
    
    if article.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    article.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.ArticleResponse)
async def update_post(id: int, updated_article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id)

    if article.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    # важно перевести объект pydantic в dict
    article.update(updated_article.dict(), synchronize_session=False)
    db.commit()
    return article.first()