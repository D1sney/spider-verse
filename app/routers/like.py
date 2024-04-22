from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/likes',
    # добавляет заголовок в документации для эндпоинтов этого роутера
    tags=['Likes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # проверяем существование поста с указанным пользователем id
    article = db.query(models.Article).filter(models.Article.id == like.article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id: {like.article_id} does not exist')
    
    # проверяем есть ли лайк на посте который указал пользователь, принадлежащий пользователю
    like_query = db.query(models.Like).filter(models.Like.article_id == like.article_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()

    if like.action == 'create_like':
        # если пользователь указал create_like (он хочет поставить лайк) и он уже ставил лайк на этот пост, выводим ошибку
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already liked article {like.article_id}')
        # если же он не ставил лайк на этот пост то мы создаем такой лайк и сохраняем его в бд
        new_like = models.Like(article_id = like.article_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {'message': f'successfully added like from {current_user.username} on article {new_like.article_id}'}
    else:
        # если пользователь указал remove_like (он хочет удалить лайк), но он не ставил лайк на этот пост, выводим ошибку 
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Like does not exist')
        # если же он ставил лайк на этот пост, тогда успешно удаляем его из бд
        like_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'successfully deleted vote'}
        
