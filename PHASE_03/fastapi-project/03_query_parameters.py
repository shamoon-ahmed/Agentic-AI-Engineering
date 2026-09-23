from fastapi import FastAPI

app = FastAPI()

@app.get("/cafe/coffee/{coffee_type}")
def get_coffee(coffee_type: str, size: str = "Medium", sugar: str = 20, order_type: str | None = None): # order_type is optional
    if order_type:
        return {"Order":f"{size} {coffee_type} with {sugar} sugar!", "order_type":order_type}

    return {"Order":f"{size} {coffee_type} with {sugar} sugar!"}

# notice we didn't add "size" and "sugar" in the path itself so they are not path parameters
# "size" and "sugar" are query parameters that has a default value
# so the url: /cafe/coffee/latte/ is same as /cafe/coffee/latte/?size=Medium&sugar=20
# so even if we don't pass those query parameters, their default values are considered
# query parameters in a url are shown like this: /cafe/coffee/latte/?size=Medium&sugar=20
# ? after the last / with key-value pairs separated by & character
# the values of query parameters change when we pass it explicitly
# also the order_type is an optional query parameter that defaults to None

# -------------------------------------------------
# Query Parameters Type Conversions & Muliple Query and Path Parameters

@app.get("/users/{user_id}/items/{item_id}")
def read_item(user_id: str, item_id: str, q: str | None = None, short: bool = False):

    item = {"user_id":user_id, "item_id":item_id}

    if q:
        item.update({"q":q})
    
    if not short: # evaluates to True
        return {"description":"this is a long description"}

# so the special feature here is:
# if we pass: yes, Yes true, 1, True, On, on..they all evalues to True
# if we pass: no, No, false, 0, False, Off, off...they all evalues to False

# also we can pass a required query parameter without passing a default value to it