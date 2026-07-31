# Learning Pydantic

Pydantic is a Python library for type and data validation/parsing

## There are different tools (functions/classes) that Pydantic Offers
- **BaseModel** : *contains logic for data/type validation*

```powershell
from pydantic import BaseModel, Field, EmailStr, AnyUrl

class Patient(BaseModel):
    name: str
    age: age
```

- **Field** : *used to define metadata for user to understand better what they need to fill in the field*

```powershell
age : int = Field(title='Age', description='Age of Patient as in the NIC', gt=0, lt=120)
```

- **Custom Types** *like **EmailStr** to validate correct email, **AnyUrl** to validate correct url*

```powershell
class Patient(BaseModel):
    linkedin_url : AnyUrl
    email: EmailStr
```

## List, Dict, Optional, Annotated

- **List and Dict Concept:**
<br>
For advance type checking, we use List, Dict, Optional, Annotated, etc to validate types
<br>
For instance, we want the user to pass a list with str elements in it. But how do we validate it?
<br>

We can say **contact : list** , but we don't know what data type is user going to insert in the list and we want string in it. We're just saying that it should be a list. That's it.
<br>
Instead we need to import List from typing module to validate it
<br>

We can say **contact : List[str]** to validate the elements inside the list should be in string format. Similarly for different type validations we do the same thing and we import the respective data type from typing.

<br>

```powershell
contact : Dict[str, str]
siblings_names : List[str]
```


- **Optional:**
<br>
We use Optional when we are saying some field is optional for the user. If they don't define it, we set a default value instead.
<br>
When using Optional, it's important to set a default value as well
<br>

```powershell
contact : Optional[Dict[str, str]] = None
married : Optional[bool] = False
```

- **Annotated:**
<br>
We use Annotated mostly with Field(), defining the metadata and the data type. That metadata could be a string or a data validation function like Field(), Query(), etc.
<br>
It should look like this. Annotated[datatype, Field()]
<br>
The default value can be defined after Annotated[] like Annotated[] = None OR in the Field(default=)
<br>

```powershell
contact : Annotated[Optional[Dict[str, str]], Field()] = None
married : Annotated[Optional[bool], Field(default=False, description="Should be correct as in the NIC")]
```

## Field Validator - @field_validator:

**@field_validator** is a decorator used with Pydantic to validate a certain field. Without @field_validator we would have to type checking, coerce data, apply constraints, etc manually. With **@field_validator**, we write our own logic to validate a certain field, raise custom error messages, etc.

We use **@field_validator** as a decorator above the function and pass the field in 'quotes' that we want to validate

```powershell
from pydantic import BaseModel, field_validator

class Patient(BaseModel):
    email : str

    @field_validator('email')
    def validate_email(value):

        valid_domains = ['piaic.com', 'smiu.edu']

        domain = value.split('@')[-1]

        if domain in valid_domains:
            return value
        raise ValueError('Unregistered Email!')
```

### mode='before' OR mode='after'

**mode** tells Pydantic when to validate and coerce the field.
For instance when converting "30" into 30, we tell Pydantic if we want the raw input "30" so we say mode='before'.
This brings us the unvalidated and non-coerced data. On the other hand mode='after' brings the coerced data.

Remember: By default, mode is after. mode='after'

```powershell
@field_validator('age', mode='before') # setting mode='before' means we want the value before any validation/coersion happens 
    def validate(value):
        if 0 < value < 120:
            return value
        return ValueError('Invalid Age!')
```

So, as @field_validator only allows to validate a single field, we need something that allows validation operation with multiple fields

This is where the next validator comes in

## Model Validator

**@model_validator** allows us to use the entire Pydantic model and validate any field we want.
Just need to pass the mode in the decorator and model in function, and we can write our own custom logic for validation.

Take a look at this code snippet:

```powershell
from pydantic import BaseModel, model_validator

class Patient(BaseModel):
    name : str
    age : int = Field(gt=0, lt=120)

    @model_validator(mode='after')
    def registration_eligibility_for_old(cls, model):
        if model.age >= 60 and 'emergency' not in model.contact_info:
            raise ValueError('Patients aged 60 and above must have an emergency number!')
        return model
```

*See how we used two attributes **age** and **contact_info** from **model.attribute**. We won't be able to do this with @field_validator.*

## Computed Field

**@computed_field** allows us to create a new field based on already created fields that the user provided. 
using **@computed_field**, user doesn't not have to have pass the value of that computed field. 
Instead, we compute that field using the already available attributes.
This makes that computed field not shown to the user as field to fill, but is added to the .model_dump() and json schemas and also Pydantic reads that field. 

Creating a regular method would do the work but Pydantic won't even know that there's a new computed field or method

Look at this code snippet:

```powershell
from pydantic import BaseModel, computed_field, Field
from typing import Optional

class Patient(BaseModel):
    name : str
    age : int = Field(gt=0, lt=120)
    height : Optional[float] = None
    weight : Optional[float] = None

    @computed_field
    def bmi(self) -> float:
        if self.weight and self.height:
            bmi = round(self.weight/self.height**2, 2)
            return bmi
        return None

    # This method also does same exact work but is not included in model's json schema neither Pydantic reads it.
    # That is why we use @comptuted_field for fields that are computed based on already provided fields
    def calculate_bmi(self):
        if self.weight and self.height:
            return round(self.weight/self.height**2, 2)
        return None
    
    def insert_patient(patient : Patient):
        ...
    
    patient_record = {'name':'Ali', 'age':30, ...}

    patient1 = Patient(**patient_record)
    insert_patient(patient1)
    print(patient1.model_dump()) # also shows that bmi field even tho we didn't ask the user to provide it
```

## Nested Models

Nested Models simply means creating more than one Pydantic model and using that Pydantic model defined before as the data type of the field in the next Pydantic model to get the correct data and access some parts of it if needed.

For instance, the address field in the Patient Pydantic Model accepts a Address data type (that is a Pydantic model defined above it) that helps us validate and access specific values if needed rather than building our own complex logic to extract parts from an address like the zip code.

Rather than passing address like below which is mixed up and would be hard to extract some parts of it like the state or zip code

```powershell
p1 = {'name':'Ali', 'age':25, 'gender':'male', 'address':'house no.20, karachi, sindh, 76664'}
patient1 = Patient(**p1)
```
Instead, we go with a structured way:

```powershell

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
```
Now it is
- *Organized*
- *Reusable*
- *Readable*
- *Can be validated*

## Serialization

**Serialization** means converting our Python object (Patient model) in our case, into a format that could easily be saved, transferred or sent over the network. For example sending data to frontend using FastAPI, for logs saving to a database, etc.

```powershell
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
```

*Notice that in the last, we passed ... as the value of 'name'* <br>
*Python will accept {key:value} pairs in a dictionary or [values] in a list. Not both at the same time like {'name','address': {'state'}} - This gives a SyntaxError.* <br>
*To exclude a top level field like 'name' and nested field like address['state'], we give name an Ellipsis (...) that tells is to exclude the entire field like **name : whatever the value*** <br>
*This way, the entire dictionary stays a dictionary with key:value pairs* <br>
*The Ellipsis(...) works like a placeholder*