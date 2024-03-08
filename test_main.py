from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_main_page():
    response = client.get("/")
    html = response.content.decode('utf-8')
    assert response.status_code == 200
    assert html.startswith('<!DOCTYPE html>')
    assert '<title>Spider-verse</title>' in response.text
    assert '<h1>Miles Morales</h1>' in response.text
    assert html.endswith('</html>')
    