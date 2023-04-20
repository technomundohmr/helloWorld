from typing import Optional

from pydantic import BaseModel

from fastapi import FastAPI, Body

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