from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, Возраст: 18'}


@app.get('/users')
async def get_users():
    return users


@app.post('/user/{username}/{age}')
async def add_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Ivan")],
        age: Annotated[int, Path(ge=1, le=100, description="Enter age", example="24")]):
    current_id = str((len(users) + 1))
    users[current_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {current_id} is registered"}


@app.put('/user/{user_id}/{username}/{age}')
async def update_data_user(user_id: Annotated[str, Path(min_length=1, description="Enter user ID")],
                           username: Annotated[str, Path(min_length=5, max_length=20,
                                                         description="Enter username", example="Ivan")],
                           age: Annotated[int, Path(ge=1, le=100, description="Enter age", example="24")]):
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"The user {user_id} is updated"}


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[str, Path(min_length=1, description="Enter user ID")]):
    users.pop(user_id)
    return {"message": f"The user {user_id} is deleted"}
