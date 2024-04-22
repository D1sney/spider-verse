from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/articles',
    # добавляет заголовок в документации для эндпоинтов этого роутера
    tags=['Articles']
)


@router.get('/', response_model=list[schemas.ArticleLikeResponse]) # list с маленькой буквы потому что после Python 3.9 так можно делать, а в ранних версиях необходимо было импортировать List из typing
async def get_articles(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: str | None = ''):
    # filter направлен на то чтобы пользователю показывались только принадлежащие ему посты, а не все
    # articles = db.query(models.Article).filter(models.Article.owner_id == current_user.id).filter(models.Article.title.contains(search)).limit(limit).offset(offset).all() # тут объект сессии обращается к нашим моделям и с помощью all вытягивает все значения, но после обращения к моделям можно также и менять данные в бд, а не только вытащить
    
    # здесь мы создаем на языке sqlalchemy запрос с join и подсчитываем количество лайков через group_by и count, важно обработаь полученные значения в response_model, потому что FastApi не знает что с ними делать, а Pydantic знает
    articles = db.query(models.Article, func.count(models.Like.article_id).label('likes')).join(models.Like, models.Article.id == models.Like.article_id, isouter=True).group_by(models.Article.id).filter(models.Article.owner_id == current_user.id).filter(models.Article.title.contains(search)).limit(limit).offset(offset).all()
    return articles

# response_model позволяет вернуть ответ пользователю в соответствии с нашей pydsntic моделью
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ArticleResponse)
async def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # мы добавляем отдельно user_id беря его из токена, а не из отправляемых данных пользователем - кто авторизирован, тот и создает пост
    new_article = models.Article(owner_id=current_user.id, **article.dict()) # вариант если очень много полей и вариант ниже становится затруднительным
    # new_article = models.Article(title=article.title, full_text=article.full_text, summary=article.summary)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@router.get('/{id}', status_code=200, response_model=schemas.ArticleLikeResponse)
async def get_one_article(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    article = db.query(models.Article, func.count(models.Like.article_id).label('likes')).join(models.Like, models.Article.id == models.Like.article_id, isouter=True).group_by(models.Article.id).filter(models.Article.id == id).first()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # проверка что пост который пользователь хочет удалить, принадлежит ему
    if article.Article.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not authorized to perform requested action")
    return article


# при status_code 204 нельзя вернуть json
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(models.Article.id == id)
    
    if article.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    # проверка что пост который пользователь хочет удалить, принадлежит ему
    if article.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not authorized to perform requested action")

    article.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.ArticleResponse)
async def update_post(id: int, updated_article: schemas.ArticleUpdate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(models.Article.id == id)

    if article.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    # проверка что пост который пользователь хочет обновить, принадлежит ему
    if article.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"not authorized to perform requested action")

    # важно перевести объект pydantic в dict
    article.update(updated_article.dict(), synchronize_session=False)
    db.commit()
    return article.first()