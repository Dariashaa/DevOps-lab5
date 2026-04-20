from fastapi.testclient import TestClient
import uuid
from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_create_user_success():
    '''Успешное создание нового пользователя'''
    unique_email = f"new_{uuid.uuid4().hex[:8]}@example.com"
    new_user = {
        'name': 'New User',
        'email': unique_email
    }

    last_id_before = users[-1]['id']

    response = client.post("/api/v1/user", json=new_user)
    user_id = response.json()
    assert response.status_code == 201
    assert user_id == last_id_before+1
    
    assert response.status_code == 201

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_email = users[0]['email']
    
    duplicate_user = {
        'name': 'Duplicate Name',
        'email': existing_email
    }
    
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    
    unique_email = f"delete_{uuid.uuid4().hex[:8]}@example.com"
    new_user = {
        'name': 'User To Delete',
        'email': unique_email
    }
    
    create_response = client.post("/api/v1/user", json=new_user)
    assert create_response.status_code == 201
    
    delete_response = client.delete("/api/v1/user", params={'email': unique_email})
    assert delete_response.status_code == 204
    assert delete_response.text == ""
