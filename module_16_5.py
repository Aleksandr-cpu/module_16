from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from typing import Annotated, List

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/", response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_users(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User  was not found")


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

