from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, EmailStr

from fastapi import FastAPI, Body, Query, Path, status

app = FastAPI()

class HairColor (Enum):
    white = "white"
    brown = "brown"
    blonde = "blonde"
    block = "block"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=3,
        example="Bogotá",
    )
    country: str =  Field(
        ...,
        min_length=3,
        example="Colombia",
    )

class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=3,
        max_length=255,
        example="Pepito",
        )
    last_name: str = Field(
        ..., 
        min_length=3,
        max_length=255,
        example="Perez",
        )
    age: int = Field(
        ...,
        gt=3,
        le=150,
        example=40,
    )
    email: EmailStr = Field(
        ..., 
        example="pepito@saibher.com",
    )
    
    active: bool = Field(
        example=True,
    )
    
    hair_color: Optional[HairColor] = Field(
        default=None,
        example="blonde",
        )
    
    is_married: Optional[bool] = Field(default=None)
    
    password: str = Field(
        ...,
        min_length=8,
    )
    # class Config:
    #     schema_extra = {
    #         "example" : {
    #             "first_name": "Andres felipe",
    #             "last_name" : "Rincón Gracia",
    #             "age": 28,
    #             "email" : "developer@saibher.com",
    #             "active": True,
    #             "hair_color": "blonde",
    #             "is_married" : True,
    #         }
    #     }

@app.get(
    path = "/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {
        "Hello":"world"
    }
    
    
@app.post(
    path = "/person/new", 
    response_model=Person, 
    response_model_exclude={'password'},
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(
    ...
    )):
    return person


@app.get(
    path ='/person/details',
    status_code=status.HTTP_200_OK,
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=3,
        max_length=255,
        title="person Name",
        description="This  is the person name. It must to be between 1 to 255 characters",
        example = "maria"
        ),
    age: Optional[int] = Query(
            ...,
            title="person age",
            description="This  is the person age. It's required must to be an integer",
            example=25
        )
):
    return {
        name: age
        }

@app.get(
    path = '/person/detail/{person_id}',
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="person age",
        description="This  is the person age. It's required must to be an integer",
        example=13
        )
):
    return {
        person_id: "existed",
    }
    
@app.put(
    path = "/person/{person_id}",
    status_code=status.HTTP_201_CREATED
    )
def update_person(
    person_id: int= Path(
        ...,
        title="Person ID",
        description="this is te person ID",
        gt=0,
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = person.dict()
    data = result.update(location.dict())
    return data