from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# модели sqlalchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    hero = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    full_text = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    category = Column(String, default=None)
    pubdate = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_published = Column(Boolean, server_default='TRUE', nullable=False)
    # CASCADE означает что при удалении юзера, все посты ссылающиеся на его id тоже будут удалены
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship('User') # это обращение не к названию таблицы а к названию класса модели!!!


class Like(Base):
    __tablename__ = "likes"
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
