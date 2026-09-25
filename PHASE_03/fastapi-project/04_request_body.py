from fastapi import FastAPI
from pydantic import BaseModel, computed_field
import uuid

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

    @computed_field
    def create_item_id(self) -> str:
        item_id = uuid.uuid4()
        return f"item-{item_id}"

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None
    tax: float | None = None

@app.post("/items/") # .post() used to create item
def create_item(item: Item): # here item is a Body() parameter. Explanation at the end
    item_details = item.model_dump()
    
    if item.tax:
        item_details.update({"price_after_tax": item.price + item.tax})
    
    return item_details

@app.put("/items/{item_id}") # .put() used to update item but fully. The entire pydantic model needs updation
def update_item(item_id: str, item: Item):
    return {"item_id":item_id, **item.model_dump()}

@app.patch("/items/{item_id}") # .patch() used to update only what needs updations
def update_item_details(item_id: str, item: ItemUpdate):
    updated_data = item.model_dump(exclude_unset=True) # excluding what's unset
    return {"item_id":item_id, "updated_item": updated_data}

# so there are three types of parameter signatures essentially:
# - Path() parameters
# - Query() parameters
# - Body() parameters

# Let me explain Body() parameters
# So for example when creating an account, uploading a blog post, etc. we don't send the entire payload in the URL
# www.example.com/signup/?user=sam&password=1122&age=21&bio=live-in-pak
# so this is a very bad approach, not suitable
# instead these parameters are considered as Body() parameters which are not displayed in the URL and FastAPI knows that
# FastAPI knows which parameters are Body(), Path() or Query() by looking at where it's coming from
# if a parameter has a Pydantic model type like above "item: Item", FastAPI knows its a Body() parameter
# but lets say we want just one parameter with a simple data type like "importance: int" to be a Body() parameter
# we define it explicitly saying "importance: int = Body()"