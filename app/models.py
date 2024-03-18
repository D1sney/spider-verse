from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
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