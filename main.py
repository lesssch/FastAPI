import time
from enum import Enum
from typing import Union, Optional

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
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


class DogUpdated(BaseModel):
    name: Union[str, None] = None
    pk: Union[int, None] = None
    kind: Union[DogType, None] = None


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
    if kind:
        result = [dogs_db[key] for key, value in dogs_db.items() if value.kind == kind]
    else:
        result = list(dogs_db)
    return result


@app.post("/dog")
def create_dog(dog: Dog) -> Dog:
    key = [key for key, value in dogs_db.items() if value.pk == dog.pk]
    if len(key) > 0:
        raise HTTPException(status_code=666, detail='The dog with this ID is already registered')
    else:
        dogs_db[max(dogs_db.keys()) + 1] = dog
    db_ind = len(post_db)
    post_db.append(Timestamp(id=db_ind, timestamp=time.time_ns()))
    return dog


@app.get("/dog/{pk}")
def get_dog_by_pk(pk: int) -> Dog:
    key = [key for key, value in dogs_db.items() if value.pk == pk]
    if len(key) == 0:
        raise HTTPException(status_code=404, detail='The dog is not found')
    else:
        result = [dogs_db[key] for key, value in dogs_db.items() if value.pk == pk]
    return result[0]


@app.patch("/dog/{pk}")
def update_dog(pk: int, model: Dog) -> Dog:
    key = [key for key, value in dogs_db.items() if value.pk == pk]
    if len(key) == 0:
        raise HTTPException(status_code=404, detail='The dog is not found')
    else:
        dog = dogs_db[key[0]]
        update_data = model.model_dump(exclude_unset=True)
        dog_updated = dog.model_copy(update=update_data)
        print(dog_updated)
        dogs_db[key[0]] = jsonable_encoder(dog_updated)
        db_ind = len(post_db)
        post_db.append(Timestamp(id=db_ind, timestamp=time.time_ns()))
    return dog_updated
