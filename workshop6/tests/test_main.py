from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_products_returns_200():
    response = client.get("/api/products")

    assert response.status_code == 200


def test_list_products_returns_all_products():
    response = client.get("/api/products")

    assert len(response.json()) == 3


def test_each_product_has_id_name_and_price():
    products = client.get("/api/products").json()

    for product in products:
        assert set(product) == {"id", "name", "price"}
        assert isinstance(product["price"], float)
