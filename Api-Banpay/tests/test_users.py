from app.schemas.user import UserCreate

def test_create_user(client, db):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "role": "admin"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["role"] == user_data["role"]