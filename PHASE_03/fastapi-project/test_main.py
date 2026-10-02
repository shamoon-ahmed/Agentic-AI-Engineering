from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

# app = FastAPI()

# @app.get("/home")
# async def home():
#     return {"message":"hello world home"}

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name":"watch", "price":1200.00})

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["price"], float)
    
    assert "item_id" in data
    assert data["item_id"].startswith("item-")