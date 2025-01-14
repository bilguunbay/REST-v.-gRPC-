from typing import List
from faker import Faker
from faker.providers import address
from faker.providers import date_time
from faker.providers import phone_number
from faker.providers import DynamicProvider
from pydantic import BaseModel
from datetime import date 
from enum import Enum 
from fastapi import FastAPI
from http.client import HTTPException   

fake = Faker()
app = FastAPI()

class phoneType(Enum):
    MOBILE = 'mobile'
    HOME = 'home'

class addressType(Enum):
    RESIDENTIAL = 'residential'
    BILLING = 'billing'

class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'

class Address(BaseModel):
    id: int
    zipCode: str 
    street: str
    city: str
    state: str
    type: addressType

class Contact(BaseModel):
    id: int 
    name: str
    phoneNumber: str 

class Patient(BaseModel):
    id: int 
    status: bool
    name: str 
    gender: Gender
    birthday: date 
    deceasedDate: date
    maritalStatus: bool
    preferredLang: str
    activeFrom: date
    activeThrough: date 
    addresses: List[Address]
    phoneNumbers: List[str]
    contact: List[Contact]

fake.add_provider(address)
fake.add_provider(date_time)
fake.add_provider(phone_number)

addressType = DynamicProvider(
    provider_name='tProvider',
    elements=[addressType.BILLING, addressType.RESIDENTIAL]
)

genderSelect = DynamicProvider(
    provider_name='gProvider',
    elements=['male', 'female']
)

fake.add_provider(genderSelect)
fake.add_provider(addressType)
l = []
for i in range(10):
    a = Address(
        id=1000+i,
        zipCode=fake.postcode(),
        street=fake.street_address(),
        city=fake.city(),
        state=fake.country_code(),
        type=fake.tProvider()
    )
    c = Contact(
        id = i,
        name=fake.name(),
        phoneNumber=fake.phone_number()
    )
    p = Patient(
        id=i,
        status=fake.boolean(),
        name=fake.name(),
        gender=fake.gProvider(),
        birthday=fake.date_of_birth(),
        deceasedDate=fake.date(),
        maritalStatus=fake.boolean(),
        preferredLang=fake.language_name(),
        activeFrom=fake.date(),
        activeThrough=fake.date(),
        addresses=[a],
        phoneNumbers=[fake.phone_number()],
        contact=[c]
        )
    l.append(p)

@app.get("/test")
def returner() -> List[Patient]:
    return l