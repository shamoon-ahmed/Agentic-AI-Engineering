from fastapi import FastAPI, Path
from enum import Enum
from typing import Annotated

app = FastAPI()


@app.get("/greeting/{name}")
async def say_hello(name: str):
    return {"message": f"Hey  {name}"}

# now we need to keep in mind that fastapi follows the order of apis created in the script
# here we say /users/me and /users/{user_id}
# but look w defined the fixed path first and then the dynamic path for a reason
# lets say if the apis are switched (2nd one comes first and 1st one comes second)
# if we passed "me", FastAPI will trigger the "/users/{user_id}" and return {"user":"Userme"}
# but look we actually wanted {"user":"this is the current user"}
# so this is the problem. it will use the path that matches first so order matters

@app.get("/users/me")
async def get_user():
    return {"user":"this is the current user"}

@app.get("/users/{user_id}")
async def get_user2(user_id: str):
    return {"user":f"User{user_id}"}

@app.get("/items/{item_id}")
async def get_item(item_id: Annotated[str, Path(min_length=5)]):
    return {"Item": f"Your item ID is: {item_id}"}

# --------------------------------------------------

# if we want to have some fixed values in our path parameters, we can use Enum
# we imported Enum and then we will inherit str and Enum in our class so that FastAPI knows str data type to expect

class Admin(str, Enum):
    admin1 = "lab_instructor" # this is an enum member
    admin2 = "course_instructor"
    admin3 = "external"

@app.get("/admins/{admin_name}")
async def approve_admin(admin_name: Admin):

    if admin_name is Admin.admin1:
        return {"Admin Name":admin_name, "admin_approval":f"Access approved!"}
    
    if admin_name.value == "course_instructor":
        return {"Admin Name":admin_name, "admin_approval":f"Access approved!"}
    
    return {"Admin Name":admin_name, "admin_approval":"Please talk to the course instructor"}

# --------------------------------------------------

# Path inside path
# lets say we want a file inside our path parameter like: /files/{file_path}
# so we would need the path to be like this: /files/file_path/home/docs/llms.txt
# but this can create issues for FastAPI and also if we pass: home/docs/llms.txt, we get "Details not found"
# so to steer clear of errors, we use the :path converter from Starlette

@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path":file_path}