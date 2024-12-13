from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
from pydantic import BaseModel,Field
from typing import List

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Ivan")],
        age: Annotated[int, Path(ge=1, le=100, description="Enter age", example="24")]):
    user_id = len(users) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_data_user(user_id: Annotated[int, Path(ge=1, description="Enter user ID")],
                           username: Annotated[str, Path(min_length=5, max_length=20,
                                                         description="Enter username", example="Ivan")],
                           age: Annotated[int, Path(ge=1, le=100, description="Enter age", example="24")]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User  was not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, description="Enter user ID")]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User  was not found")
