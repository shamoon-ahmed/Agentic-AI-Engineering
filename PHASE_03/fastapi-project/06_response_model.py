from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class User(BaseModel):
    username: str
    email: EmailStr
    age: int

class UserIn(User):
    password: str

@app.post("/users/signup", response_model=User)
def signup(user: UserIn):
    return user

# the response_model allows us to return what we want to actually want to return to the client
# for example when creating a user, can't just give back the User class with password as its field
# so we created two classes User and UserIn and inherited User in UserIn
# then in the path operation decorator parameter, we defined response_model=User that will output in User model format
# there are several other functionalities when working with response model / return types that we can look FastAPI docs