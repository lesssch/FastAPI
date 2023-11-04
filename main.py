from enum import Enum
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get("/")
def root():
    return


@app.post("/post")
def get_post(tms: Timestamp):
    return tms


@app.get("/dog")
def get_dog(kind: Union[DogType, None] = None) -> list:
    result = [dogs_db[key] for key, value in dogs_db.items() if value.kind == kind]
    return result


@app.post("/dog")
def create_dog(name: str, kind: str) -> Dog:
    dog = Dog()
    dog.name = name
    dog.kind = kind
    dog.pk = max(dogs_db.keys()) + 1
    return dog
