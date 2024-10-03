from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.schema import User
from app.controller.user_controller import UserController
from app.database.database import get_db

route = APIRouter(prefix='/user')

def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    return UserController(db)

@route.post('/create')
def create(
    user: User,
    user_controller: UserController = Depends(get_user_controller)
):
    try:
        user = user_controller.create(user)
        
        if user:
            return {"success": True, "detail": "User created successfully"}
        return {"success": False, "detail": "User creation failed"}
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.get('/{email}')
def get(
    email: str,
    user_controller: UserController = Depends(get_user_controller)
):
    try:
        user = user_controller.get(email)
        return user
    except Exception as e:
        raise HTTPException(400, detail=str(e))
