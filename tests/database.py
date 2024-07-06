from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app

from app.config import settings
from app.database import get_db, Base
from alembic import command


# добавляем +psycopg2 он в сравнение чем без него, отправляет запросы к бд быстрее
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)
# # строчка выше исключает необходимость в этой строчке
# # Base = declarative_base()


# # Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # заменяет зависимость, в данном случае меняет функцию по подключения к основной бд, на другую функцию
# app.dependency_overrides[get_db] = override_get_db



# в этой строчке больше нет необходимости потому что мы теперь передаем client с помощью fixture, которая выполняется при запуске теста
# client = TestClient(app)


@pytest.fixture(scope="function") # параметр scope определяет на какую область влияет один вызов fixture - например fixture может быть вызвана отдельно перед каждым тестом, перед каждым модулем с тестами, перед каждым классом и т.д. Но использование scope="module" не рекомендуется, потому что тогда тесты становятся зависимыми друг от друга, а тесты должны быть независимыми
def session():
    Base.metadata.drop_all(bind=engine) # удаляем все таблицы после тестов, важно сначала все удалить а потом все создать, а не наоборот
    Base.metadata.create_all(bind=engine) # создаем все таблицы перед тестами
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # new logic
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    
    # run our code before we run our test
    # Base.metadata.drop_all(bind=engine) # удаляем все таблицы после тестов, важно сначала все удалить а потом все создать, а не наоборот
    # или можно использовать вариант с alembic
    # command.downgrade("base")
    yield TestClient(app)
    # run our code after our test finishes
    # Base.metadata.create_all(bind=engine) # создаем все таблицы перед тестами
    # или можно использовать вариант с alembic
    # command.upgrade("head")
