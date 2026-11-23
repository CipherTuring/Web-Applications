from fastapi import FastAPI

app = FastAPI(title="Workshop 6 Products API")


PRODUCTS = [
    {"id": 1, "name": "Mechanical Keyboard", "price": 79.90},
    {"id": 2, "name": "Wireless Mouse", "price": 24.50},
    {"id": 3, "name": "27-inch Monitor", "price": 229.00},
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/products")
def list_products():
    return PRODUCTS
