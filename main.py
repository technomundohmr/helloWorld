from typing import Optional

from pydantic import BaseModel

from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    active: bool
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {
        "Hello":"world"
    }
    
    
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


@app.get('/person/details')
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=3,
        max_length=255,
        title="person Name",
        description="This  is the person name. It must to be between 1 to 255 characters",
        ),
    age: Optional[int] = Query(
        ...,
        title="person age",
        description="This  is the person age. It's required must to be an integer"    
        )
):
    return {
        name: age
        }

@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="person age",
        description="This  is the person age. It's required must to be an integer"    
        )
):
    return {
        person_id: "existed",
    }