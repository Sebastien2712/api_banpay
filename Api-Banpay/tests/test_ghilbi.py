from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_consume_ghibli_api():
    # Crear un usuario con rol "films"
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "role": "films"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Consumir la API de Studio Ghibli con un recurso permitido
    response = client.get(f"/users/{user_id}/ghibli/films")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Intentar consumir un recurso no permitido
    response = client.get(f"/users/{user_id}/ghibli/people")
    assert response.status_code == 403
    assert response.json()["detail"] == "User with role 'films' is not allowed to access 'people'"