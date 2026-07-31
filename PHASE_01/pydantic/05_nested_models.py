from pydantic import BaseModel

class Address(BaseModel):

    city : str
    state : str
    zip : int

class Patient(BaseModel):

    name : str
    age : int
    gender : str
    address : Address

# We can pass values like this
p1 = {'name':'Ali', 'age':25, 'gender':'male', 'address':{'city':'Karachi', 'state':'Sindh', 'zip':75850}}
patient1 = Patient(**p1)

# Or like this
patient2 = Patient(name='Ali', age=30, gender='male', address=Address(city='Karachi', state='Sindh', zip=76666))

print(patient1.name)
print(patient1.address.zip)