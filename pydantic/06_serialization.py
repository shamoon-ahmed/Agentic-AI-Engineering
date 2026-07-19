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

p1 = {'name':'Ali', 'age':25, 'gender':'male', 'address':{'city':'Karachi', 'state':'Sindh', 'zip':75850}}
patient1 = Patient(**p1)

print(patient1.name)
print(patient1.address.zip)

# Exporting / Serialization

p1_data = patient1.model_dump() # gives a dict object
print(p1_data)
print(type(p1_data))

p1_data_json = patient1.model_dump_json() # gives a JSON string object 
print(p1_data_json)
print(type(p1_data_json))

# Some parameters to control the serialization
p1_data = patient1.model_dump(include=['name', 'age'])
print(p1_data)

p1_data = patient1.model_dump(exclude=['age'])
print(p1_data)

p1_data = patient1.model_dump(exclude={'name':...,'address': {'state'}})
print(p1_data)