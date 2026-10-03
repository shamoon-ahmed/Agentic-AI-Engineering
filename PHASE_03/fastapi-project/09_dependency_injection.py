from fastapi import Depends, FastAPI, Header, HTTPException, status

app = FastAPI()

# fake db
authenticated_users = {
    "admin-223344":{"user":"shamoon", "role":"developer"},
    "user-223344":{"user":"sam", "role":"designer"}
}

def authenticate_user(token: str = Header()):
    if token not in authenticated_users:
        raise HTTPException(status_code=401, detail="Unauthenticated user")
    
    return authenticated_users[token]

@app.get("/authenticate")
def authenticate(user = Depends(authenticate_user)):
    return user
