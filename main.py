from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("a272b36b-de38-474f-94f8-b1ad0eedea2e"),
        first_name="Cavad",
        gender = Gender.male,
        roles = [Role.student]
    )
]

@app.get("/")
def root():
    return {"Hello" : "World"}

@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register(user: User):
    db.append(user)
    return {"id" : user.id}
    
@app.delete("/api/v1/users/{user_id}")
async def delete(user_id : UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return db

@app.put("/api/v1/users/{user_id}")
async def update(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name 
            if user_update.gender is not None:
                user.gender = user_update.gender 
            if user_update.roles is not None:
                user.roles = user_update.roles 
            return user
    raise HTTPException(
        status_code=404, 
        detail=f"user with id: {user_id} does not exists"
    )