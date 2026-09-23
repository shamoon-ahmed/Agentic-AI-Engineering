from fastapi import FastAPI

app = FastAPI()

@app.get("/") # @app = path operation decorator, .get() = path operation
async def root(name: str): # path operation function
    return {"message": f"Hello world!"}

# after deploying with: fastapi deploy
# the app is available at: https://say-hello.fastapicloud.dev/
# say-hello is the directory I named it when configuring the deployment in the terminal