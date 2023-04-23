import pytest
from fastapi.testclient import TestClient

from revendeurapi.main import app, db


# @pytest.fixture
# def db():
#    with Db(':memory:', clear=True) as db:
#        db.create_tables()
#        yield db
#    return db


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def user_token(client):
    db.delete_user(99)
    headers = {"Authorization": "Bearer admin"}
    response = client.post("/api/v1/create-user/99/test%40test.com", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": "success",
                               "message": "User with id 99 has been created. Check your email for the QR code"}
    token_ = db.get_user(99)[2]
    return token_


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the MSPR API"}


def test_get_products(client, user_token):
    headers = {"Authorization": "Bearer " + user_token}
    response = client.get("/api/v1/products", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_product_does_not_exist(client, user_token):
    headers = {"Authorization": "Bearer " + user_token}
    response = client.get("/api/v1/products/1", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {'status': 'error', 'message': 'Product not found'}


def test_get_product_exists(client, user_token):
    headers = {"Authorization": "Bearer " + user_token}
    response = client.get("/api/v1/products/5", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {'createdAt': '2023-02-20T01:12:28.696Z', 'name': 'Jacquelyn Hyatt',
                               'details': {'price': '662.00',
                                           'description': 'Andy shoes are designed to keeping in mind durability as well as trends, the most stylish range of shoes & sandals',
                                           'color': 'violet'}, 'stock': 67002, 'id': '5'}


def test_get_product_stock_does_not_exist(client, user_token):
    headers = {"Authorization": "Bearer " + user_token}
    response = client.get("/api/v1/products/1/stock", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {'status': 'error', 'message': 'Product not found'}


def test_get_product_stock_exists(client, user_token):
    headers = {"Authorization": "Bearer " + user_token}
    response = client.get("/api/v1/products/5/stock", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == int
    assert response.json() == 67002


if __name__ == '__main__':
    pytest.main(['-v'])
