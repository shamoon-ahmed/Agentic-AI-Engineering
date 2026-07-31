from pydantic import BaseModel, AnyUrl, Field, field_validator
from typing import List, Dict, Annotated, Optional

# Inheriting BaseModel for type and data validation
class Patient(BaseModel):
    name : str
    age : int
    married : Optional[bool] = None
    linkedin_url : AnyUrl
    email : str
    allergies : Optional[List[str]] = None
    contact_info : Dict[str, str]

    # Suppose we need to verify if an email contains a certain domain name. If it matched the domain that we want, we continue
    # Otherwise, we raise an error

    @field_validator('email')
    def validate_email(value):
        # if 'piaic.com' in value or 'smiu.edu' in value and 'gmail.com' not in value:
        #     return value
        # raise ValueError('Not a registered person! Only accepting people from PIAIC and SMIU')
        valid_domains = ['piaic.com', 'smiu.edu']

        domain = value.split('@')[-1]

        if domain in valid_domains:
            return value
        return ValueError('Unregistered Email!')

    @field_validator('age', mode='after') # setting mode='before' means we want the value before any validation/coersion happens 
    def validate(value):
        if 0 < value < 120:
            return value
        return ValueError('Invalid Age!')


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
                  'age':130,
                  'linkedin_url':'http://linkedin.com/shamoon-ahmed',
                  'email': 'sam@gmail.com',
                  'contact_info':{'phone':'23456'}}

# creating the patient object with patient record and then unpacking it
# ** means it converts a dict into keyword arguments
patient1 = Patient(**patient_record) # this is where validation and coersion happens 
# (coersion means converting a certain data type to another data type. For e.g: "30" into 30)

insert_patient(patient1)