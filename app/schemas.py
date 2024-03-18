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
