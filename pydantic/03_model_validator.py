from pydantic import BaseModel, AnyUrl, Field, model_validator
from typing import List, Dict, Annotated, Optional

# Inheriting BaseModel for type and data validation
class Patient(BaseModel):
    name : str
    age : int = Field(gt=0, lt=120)
    married : Optional[bool] = None
    linkedin_url : AnyUrl
    email : str
    allergies : Optional[List[str]] = None
    contact_info : Dict[str, str]

    @model_validator(mode='after')
    def registration_eligibility_for_old(cls, model):
        if model.age >= 60 and 'emergency' not in model.contact_info:
            raise ValueError('Patients aged 60 and above must have an emergency number!')
        return model


# Creating a function that accepts a Patient object. That patient object is defined later
def insert_patient(patient : Patient):
    print("Patient's Name: ", patient.name)
    print("Patient's Age: ", patient.age)
    print("Patient's Allergies: ", patient.allergies)
    print("Patient's Email: ", patient.email)
    print("Patient's Linkedin: ", patient.linkedin_url)
    print("Patient's Contact: ", patient.contact_info)
    print("Patient's Married Status: ", patient.married)

    print("-- Patient Record Inserted! --")

# the new patient record. Pydantic will automatically convert string number into int if passed incorrectly passed
patient_record = {'name':'Ali',
                  'age':60,
                  'linkedin_url':'http://linkedin.com/shamoon-ahmed',
                  'email': 'sam@gmail.com',
                  'contact_info' : {'phone':'22334455', 'emergency':'22222'}}

# creating the patient object with patient record and then unpacking it
# ** means it converts a dict into keyword arguments
patient1 = Patient(**patient_record) # this is where validation and coersion happens 
# (coersion means converting a certain data type to another data type. For e.g: "30" into 30)

insert_patient(patient1)