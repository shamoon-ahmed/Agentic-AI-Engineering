from fastapi import FastAPI

app = FastAPI()

@app.get("/") # @app = path operation decorator, .get() = path operation
async def root(name: str): # path operation function
    return {"message": f"Hello {name}!"}