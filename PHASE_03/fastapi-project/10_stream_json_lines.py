from collections.abc import AsyncIterable
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: int

items = [
    Item(name="watch", price=1200),
    Item(name="book", price=200),
    Item(name="belt", price=300)
]

@app.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item