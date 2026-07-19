from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Annotated, Optional

# Inheriting BaseModel for type and data validation
class Patient(BaseModel):
    name : Annotated[str, Field(max_length=30, title='Name of Patient', description='Name registered in CNIC', examples='Rengoku')]
    age : int = Field(gt=0, lt=110, strict=True) # As pydantic converts str numbers into int automatically, sometimes its not useful. So we can restrict a specific field to not convert a str number into in but saying strict=True. Now if we pass age as '20', the program will throw an error and will only work if correct int is passed in int format
    married : Annotated[Optional[bool], Field(default=False)] # If no value is passed, it defaults to False 
    linkedin_url : AnyUrl
    email: EmailStr
    allergies : Optional[List[str]] = None 
    contact_info : Annotated[Dict[str, str], Field(title='Your Phone #', description='Your contact details')]


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
                  'age':30,
                  'linkedin_url':'http://linkedin.com/shamoon-ahmed',
                  'email': 'sam@gmail.com',
                  'contact_info':{'phone':'23456'}}

# creating the patient object with patient record and then unpacking it
# ** means it converts a dict into keyword arguments
patient1 = Patient(**patient_record)

insert_patient(patient1)