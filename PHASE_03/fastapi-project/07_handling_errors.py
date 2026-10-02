from fastapi import FastAPI, HTTPException, status

app = FastAPI()

items = {"watch":"very precious"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found! Make sure ID is correct!")
    
    return items[item_id]
    
