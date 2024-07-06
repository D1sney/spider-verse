# Все fixture которые находятся в этом файле, в файле с таким именем, ненужно импортировать чтобы к ним обратиться, они доступны для вызова по умолчанию

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app

from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
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


# эта fixture создает пользователя для теста с логированием пользователя, так как для этого теста необходимо иметь в бд пользователя
@pytest.fixture
def test_user(client):
    user_data = {"username": "Kolya", "hero": "Venom", "email": "hello12@gmail.com", "password": "12345"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

# второй юзер необходим для проверки функциаонала, что пользователь не может удалять чужие посты
@pytest.fixture
def test_user2(client):
    user_data = {"username": "Nikita", "hero": "Goblin", "email": "hello11@gmail.com", "password": "12345"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

# эта fixture с помощью нашей импортированной функции создает токен для тестирования, на данных тестового user из бд
@pytest.fixture
def token(test_user):
    return create_access_token({"username": test_user['email']})

# эта fixture добавляет в заголовки нашего клиента токен авторизации и теперь клиент может делать запросы к страницам требующим авторизации
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_articles(test_user, test_user2, session):
    articles_data = [{
        "title": "1st title",
        "full_text": "1st full",
        "summary": "1st sum",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "full_text": "2nd full",
        "summary": "2nd sum",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "full_text": "3rd full",
        "summary": "3rd sum",
        "owner_id": test_user['id']
    }, {
        "title": "4th title",
        "full_text": "4th full",
        "summary": "4th sum",
        "owner_id": test_user2['id']
    }]
    # превращает dict с данными об одном заголовке в sqlalchemy модель
    def create_article_model(article):
        return models.Article(**article)
    # проходится по articles_data и каждый dict пропускает через функцию create_article_model
    articles = list(map(create_article_model, articles_data))

    session.add_all(articles)
    session.commit()
    return session.query(models.Article).all()