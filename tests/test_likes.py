import pytest
from app import models


# мы пишем данную fixture здесь, а не в conftest, только потому что она будет использоваться только здесь, а другим тестам она не нужна, и смысла писать в conftest особо нет, но в целом без разницы
@pytest.fixture
def test_like(test_articles, session, test_user):
    new_like = models.Like(article_id=test_articles[3].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()


def test_like_create(authorized_client, test_articles):
    response = authorized_client.post("/likes/", json={"article_id": test_articles[0].id, "action": "create_like"})
    assert response.status_code == 201


def test_like_twice(authorized_client, test_articles, test_like):
    response = authorized_client.post("/likes/", json={"article_id": test_articles[3].id, "action": "create_like"})
    assert response.status_code == 409


def test_like_remove(authorized_client, test_articles, test_like):
    response = authorized_client.post("/likes/", json={"article_id": test_articles[3].id, "action": "remove_like"})
    assert response.status_code == 201


def test_like_remove_not_exist(authorized_client, test_articles):
    response = authorized_client.post("/likes/", json={"article_id": test_articles[3].id, "action": "remove_like"})
    assert response.status_code == 404


def test_like_create_on_article_not_exist(authorized_client, test_articles):
    response = authorized_client.post("/likes/", json={"article_id": 55555, "action": "create_like"})
    assert response.status_code == 404


def test_like_unauthorized_user(client, test_articles):
    response = client.post("/likes/", json={"article_id": test_articles[0].id, "action": "create_like"})
    assert response.status_code == 401