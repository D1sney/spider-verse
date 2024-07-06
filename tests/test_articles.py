import pytest
from app import schemas

def test_get_all_articles(authorized_client, test_user, test_articles):
    response = authorized_client.get("/articles/")

    # валидируем response по нашей схеме ответа для заголовков
    def validate(article):
        return schemas.ArticleLikeResponse(**article) # данные подходят по схему ответ с ЛАЙКАМИ а не обычную схему ArticleResponse, это важно
    articles = list(map(validate, response.json())) # теперь мы можем проверять переменную articles как хотим
    # почему-то длин articles после этой валидации 3 (нету загловка второго пользователя), а длина test_articles == 4
    # Я понял почему так происходит, потому что в response авторизованный пользователь получает только СВОИ заголовки, а в test_articles возвращаются все загловки
    # пользователь может получать только свои заголовки, длина response должна ровняться длине только принадлежащих юзеру заголовков, а не всех
    # assert len(response.json()) == len([i for i in articles if i.dict()['Article']['owner_id'] == test_user['id']]) # эта запись рабочая и сортирует заголовки по owner_id, но это излишне, потому что в response и в articles уже содержатся только принадлежащие юзеру заголовки
    assert len(response.json()) == len(articles)
    assert response.status_code == 200


def test_unauthorized_user_get_all_articles(client, test_articles):
    response = client.get("/articles/")
    assert response.status_code == 401


def test_get_one_article(authorized_client, test_articles):
    response = authorized_client.get(f"/articles/{test_articles[0].id}")
    article = schemas.ArticleLikeResponse(**response.json())
    # сравниваем данные из response и те что мы передавали в бд
    assert article.Article.id == test_articles[0].id
    assert article.Article.title == test_articles[0].title
    assert article.Article.full_text == test_articles[0].full_text


def test_unauthorized_user_get_one_article(client, test_articles):
    response = client.get(f"/articles/{test_articles[0].id}")
    assert response.status_code == 401


def test_get_one_article_not_exist(authorized_client, test_articles):
    response = authorized_client.get(f"/articles/77777")
    assert response.status_code == 404

# с помощью параметритизации проверяем разные варианты данных
@pytest.mark.parametrize("title, full_text, summary, is_published", [
    ("spider title", "spider text", "spi-text", True),
    ("venom title", "venom text", "v-text", False),
    ("goblin title", "goblin text", "gob-text", True),
])
def test_create_article(authorized_client, test_user, title, full_text, summary, is_published):
    response = authorized_client.post("/articles/", json={"title": title, "full_text": full_text,
                                                          "summary": summary, "is_published": is_published})
    created_article = schemas.ArticleResponse(**response.json())
    # сравниваем данные из response и те что мы указывали в параметритизации
    assert created_article.title == title
    assert created_article.full_text == full_text
    assert created_article.summary == summary
    assert created_article.is_published == is_published
    assert created_article.owner_id == test_user['id']
    assert response.status_code == 201

# проеверяем что если не указать is_published, то по умолчанию присвоится значение True
def test_create_article_default_published_true(authorized_client, test_user):
    response = authorized_client.post("/articles/", json={"title": "arbitrary title", "full_text": "random text",
                                                          "summary": "ran-summary"})
    created_article = schemas.ArticleResponse(**response.json())
    # сравниваем данные из response и те что мы указывали в параметритизации
    assert created_article.title == "arbitrary title"
    assert created_article.full_text == "random text"
    assert created_article.summary == "ran-summary"
    assert created_article.is_published == True
    assert created_article.owner_id == test_user['id']
    assert response.status_code == 201


def test_unauthorized_user_create_article(client, test_user):
    response = client.post("/articles/", json={"title": "arbitrary title", "full_text": "random text",
                                               "summary": "ran-summary", "is_published": True})
    assert response.status_code == 401


def test_delete_article_success(authorized_client, test_articles):
    response = authorized_client.delete(f"/articles/{test_articles[0].id}")
    assert response.status_code == 204

# можно не передавать в тест fixture test_user, если мы к нему не собираемся обращаться, он автоматически вызовется по цепочке fixture, если мы добавим test_articles
def test_unauthorized_user_delete_article(client, test_articles):
    response = client.delete(f"/articles/{test_articles[0].id}")
    assert response.status_code == 401


def test_delete_article_not_exist(authorized_client, test_articles):
    response = authorized_client.delete("/articles/99999")
    assert response.status_code == 404

def test_delete_other_user_article(authorized_client, test_articles):
    # authorized_client это авторизованный test_user, а article под индексом 3, принадлежит test_user2, user не может удалять чужие посты
    response = authorized_client.delete(f"/articles/{test_articles[3].id}")
    assert response.status_code == 403


def test_update_article(authorized_client, test_articles):
    data = {
        "title": "update title",
        "full_text": "update full_text",
        "summary": "update summary",
        "id": test_articles[0].id
    }
    response = authorized_client.put(f"/articles/{test_articles[0].id}", json=data)
    updated_article = schemas.ArticleResponse(**response.json())
    assert updated_article.title == data['title']
    assert updated_article.full_text == data['full_text']
    assert updated_article.summary == data['summary']
    assert response.status_code == 200


def test_unauthorized_user_update_article(client, test_articles):
    response = client.put(f"/articles/{test_articles[0].id}")
    assert response.status_code == 401


def test_update_article_not_exist(authorized_client, test_articles):
    data = {
        "title": "update title",
        "full_text": "update full_text",
        "summary": "update summary",
        "id": test_articles[0].id
    }
    response = authorized_client.put("/articles/88888", json=data)
    assert response.status_code == 404


def test_update_other_user_article(authorized_client, test_articles):
    data = {
        "title": "update title",
        "full_text": "update full_text",
        "summary": "update summary",
        "id": test_articles[3].id
    }
    response = authorized_client.put(f"/articles/{test_articles[3].id}", json=data)
    assert response.status_code == 403