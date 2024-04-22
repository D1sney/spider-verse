from pydantic import BaseModel, EmailStr
import datetime
from typing import Literal



class UserCreate(BaseModel):
    username: str
    hero: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    hero: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# модели pydantic
class ArticleBase(BaseModel):
    title: str
    full_text: str
    summary: str
    category: str | None = None
    is_published: bool = True

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    pubdate: datetime.datetime | None = None
    owner_id: int
    owner: UserResponse # благодаря relationship, sqlalchemy сама отлавливает пользователя, а с помощью pydantic модели мы можем ссылаться на другую модель и получится вложенный json в ответе

    class Config:
        from_attributes = True

# это модель для ответа на запрос с join и тут важно использовать такие же названия как в запросе к бд, чтобы все работало
class ArticleLikeResponse(BaseModel):
    Article: ArticleResponse
    likes: int

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str

# называется data а не response потому что отвечает за модель ответа в функции а не в эндпоинте
# cхема включает в себя то что мы передаем в токен
class TokenPayload(BaseModel):
    username: str | None = None



class Like(BaseModel):
    article_id: int
    action: Literal['create_like', 'remove_like'] # action принимает только значение из списка