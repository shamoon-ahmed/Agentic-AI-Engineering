from pydantic import BaseModel, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated

# Inheriting BaseModel for type and data validation
class Patient(BaseModel):
    name : str
    age : int = Field(gt=0, lt=120)
    height : Optional[float] = None
    weight : Optional[float] = None
    married : Optional[bool] = None
    email : str
    allergies : Optional[List[str]] = None
    contact_info : Dict[str, str]

    @computed_field
    def bmi(self) -> float:
        if self.weight and self.height:
            bmi = round(self.weight/self.height**2, 2)
            return bmi
        return None

    # This method also does same exact work but is not included in model's json schema neither Pydantic reads it.
    def calculate_bmi(self):
        if self.weight and self.height:
            return round(self.weight/self.height**2, 2)
        return None

# Creating a function that accepts a Patient object. That patient object is defined later
def insert_patient(patient : Patient):
    print("Patient's Name: ", patient.name)
    print("Patient's Age: ", patient.age)
    print("Patient's Height: ", patient.height)
    print("Patient's Weight: ", patient.weight)
    print("Patient's BMI: ", patient.calculate_bmi())
    print("Patient's Allergies: ", patient.allergies)
    print("Patient's Email: ", patient.email)
    print("Patient's Contact: ", patient.contact_info)
    print("Patient's Married Status: ", patient.married)

    print("-- Patient Record Inserted! --")

# the new patient record. Pydantic will automatically convert string number into int if passed incorrectly passed
patient_record = {'name':'Ali',
                  'age':60,
                  'height':1.72,
                  'weight':55,
                  'email': 'sam@gmail.com',
                  'contact_info' : {'phone':'22334455', 'emergency':'22222'}}

# creating the patient object with patient record and then unpacking it
# ** means it converts a dict into keyword arguments
patient1 = Patient(**patient_record) # this is where validation and coersion happens 
# (coersion means converting a certain data type to another data type. For e.g: "30" into 30)

insert_patient(patient1)
print(patient1.model_dump()) # also shows that bmi field even tho we didn't ask the user to provide it