from pydantic import BaseModel
import datetime

# модели pydantic
class User(BaseModel):
    id: int
    username: str
    hero: str
    email: str
    password: str


class ArticleBase(BaseModel):
    id: int
    title: str
    full_text: str
    summary: str
    category: str | None = None
    pubdate: datetime.datetime | None = None
    is_published: bool = True

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleResponse(BaseModel):
    id: int
    title: str
    full_text: str
    summary: str
    category: str | None = None
    # Pydantic orm_mode сообщит модели Pydantic читать данные, даже если это не модель dict, 
    # а модель ORM (или любой другой произвольный объект с атрибутами)
    class Config:
        orm_mode = True