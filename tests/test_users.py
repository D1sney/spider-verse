import pytest
import jwt
from app import schemas
# from .database import client, session # мы должны импортировать session даже если мы к нему не обращаемся в тестах, потому что client вызывает session и это необходимо для корректной работы
from app.config import settings



# теперь, когда у нас две fixture, отдельно под объект клиента и отдельно под объект бд, мы можем отдельно обращаться к ним в тесте
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_user(client):
    # супер важно указывать в конце пути слэш - "/users/", Если указывать без слеша, то FastApi по умолчанию перенаправит на адресс с слешом в конце, а это означает что мы получим статуст код 307 reidrect, и наш тест не пройдет проверку, поэтому в тесте важно сразу указывать точный адресс, со слэшем в конце
    response = client.post("/users/", json={"username": "Kolya", "hero": "Venom", "email": "hello12@gmail.com", "password": "12345"})
    # валидируем response по pydantic схеме
    response_user = schemas.UserResponse(**response.json())
    assert response_user.email == 'hello12@gmail.com'
    assert response.status_code == 201

def test_login_user(test_user, client):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']}) # здесь мы используем data вместо json потому что так передаются данные в нашем приложении по адрессу login
    login_response = schemas.Token(**response.json())
    # декодируем токен из респонса
    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    # получаем из токена лежащую в нем почту под ключом username
    username = payload.get('username')
    # сравниваем лежащую в токене почту с почтой из нашего словаря в test_user fixture
    assert username == test_user['email']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

# с помощью параметритизации проверяем разные варианты событий
@pytest.mark.parametrize("email, password, status_code", [
    ("wrongEmail@gmail.com", "12345", 403),
    ("hello12@gmail.com", "wrongPassword", 403),
    ("wrongEmail@gmail.com", "wrongPassword", 403),
    (None, "12345", 422),
    ("hello12@gmail.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password}) # здесь мы используем data вместо json потому что так передаются данные в нашем приложении по адрессу login
    assert response.status_code == status_code
    # assert response.json().get('detail') == 'Invalid Credentials' # Invalid Credentials подходит только для 403 статус кода