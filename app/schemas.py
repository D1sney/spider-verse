from pydantic import BaseModel, EmailStr
import datetime

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

    class Config:
        from_attributes = True


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


class Token(BaseModel):
    access_token: str
    token_type:str

# называется data а не response потому что отвечает за модель ответа в функции а не в эндпоинте
# cхема включает в себя то что мы передаем в токен
class TokenPayload(BaseModel):
    username: str | None = None
