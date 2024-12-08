from fastapi import FastAPI

app =FastAPI()

@app.get("/user/admin")
async def admin():
    return {"message: Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def user(user_id: int):
    return {f"message: Вы вошли как пользователь № {user_id}"}

@app.get("/user")
async def user_info(username: str = None, age: int = None):
    return {f"message: Информация о пользователе. Имя: {username}, Возраст: {age}"}

@app.get("/")
async def root():
    return  {"message: Главная страница"}