from fastapi import FastAPI, Header, Path, Body
from pydantic import BaseModel, computed_field
import uuid

app = FastAPI()

class Item(BaseModel):
    title: str
    price: float

    @computed_field
    def create_item_id(self) -> str:
        item_id = uuid.uuid4()
        return f"item-{item_id}"

class UpdateItem(BaseModel):
    title: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    item_details = item.model_dump()

    return item_details

@app.put("/items/update_item/{item_id}")
def update_item(
    item_id: str = Path(),
    item_data: UpdateItem = ...,
    token: str = Header(description= "Admin bearer token") # this is a header. Explanation below
    ):
    return {
        "message":"item_updated",
        "item_id":item_id,
        "updated_item":item_data,
        "auth_token": token
    }

# so Headers are like labels on a request
# when our client (a web browser for instance) sends a web request on a server, it has a couple things associated with it:
# - the path with path parameters: store.com/items/read_item/{item_id}
# - any query parameters (after ?): store.com/items/read_item/{item_id}?results=10&sort=alphabetically
# - the body/payload: this is not displayed in the URL, it is the actual data sent in the HTTP message
# - headers: these are labels that are attached with the web request that tells the server where this request is coming from, what language it is or is supposed to send in, any  auth tokens, etc.
# 
# this is what a raw HTTP message looks like where before the line space are the headers, after is the body/payload:
# 
# GET /items
# Host: store.com
# Content-Type: application/json
# Authorization: Bearer secret-token-123 

# {"name": "Espresso Machine", "price": 250} # this is the body/payload