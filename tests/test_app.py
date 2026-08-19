import pytest

from server.app import app
from server.models import initialize_database, get_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True

    initialize_database()

    with app.test_client() as client:
        yield client


def clear_database():
    connection = get_connection()
    connection.execute("DELETE FROM inventory")
    connection.commit()
    connection.close()


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Inventory Management API"


def test_get_inventory(client):
    clear_database()

    response = client.get("/inventory")

    assert response.status_code == 200
    assert response.get_json() == []


def test_add_inventory_item(client):
    clear_database()

    response = client.post(
        "/inventory",
        json={
            "name": "Milk",
            "barcode": "123456789",
            "quantity": 20,
            "price": 120
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Milk"
    assert data["barcode"] == "123456789"
    assert data["quantity"] == 20
    assert data["price"] == 120


def test_get_inventory_item(client):
    clear_database()

    response = client.post(
        "/inventory",
        json={
            "name": "Bread",
            "barcode": "987654321",
            "quantity": 15,
            "price": 80
        }
    )

    item_id = response.get_json()["id"]

    response = client.get(
        f"/inventory/{item_id}"
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "Bread"


def test_get_missing_inventory_item(client):
    response = client.get("/inventory/99999")

    assert response.status_code == 404


def test_update_inventory_item(client):
    clear_database()

    response = client.post(
        "/inventory",
        json={
            "name": "Juice",
            "barcode": "111111111",
            "quantity": 10,
            "price": 200
        }
    )

    item_id = response.get_json()["id"]

    response = client.put(
        f"/inventory/{item_id}",
        json={
            "quantity": 25,
            "price": 250
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["quantity"] == 25
    assert data["price"] == 250
    assert data["name"] == "Juice"


def test_delete_inventory_item(client):
    clear_database()

    response = client.post(
        "/inventory",
        json={
            "name": "Water",
            "barcode": "222222222",
            "quantity": 30,
            "price": 50
        }
    )

    item_id = response.get_json()["id"]

    response = client.delete(
        f"/inventory/{item_id}"
    )

    assert response.status_code == 200

    response = client.get(
        f"/inventory/{item_id}"
    )

    assert response.status_code == 404