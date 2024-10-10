from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from app.database.schema import User, UserResponse, ErrorResponse
from app.controller.user_controller import UserController
from app.database.database import get_db

route = APIRouter(prefix='/user')

def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    return UserController(db)

@route.post('/create', responses={500: {"model": ErrorResponse}})
def create(
    user: Annotated[User, Query()] = ...,
    user_controller: UserController = Depends(get_user_controller)
):
    try:
        return user_controller.create(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.get('/{email}', responses={500: {"model": ErrorResponse}})
def get(
    email: str = Path(regex=r'^\S+@\S+\.\S+$'),
    user_controller: UserController = Depends(get_user_controller)
):
    try:
        if user := user_controller.get(email):
            return {"success": True, "user name": user.name}
        raise HTTPException(404, detail="User not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.get('/users/list', response_model=Page[UserResponse], responses={500: {"model": ErrorResponse}})
def get_all(
    user_controller: UserController = Depends(get_user_controller)
):
    try:
        users = user_controller.get_all()
        return paginate(users)
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.put('/update', responses={500: {"model": ErrorResponse}})
def update(
    user: Annotated[User, Query()] = ...,
    user_controller: UserController = Depends(get_user_controller)
):
    try:
        return user_controller.update(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.delete('/delete', responses={500: {"model": ErrorResponse}})
def delete(
    email: Annotated[str, Query(regex=r'^\S+@\S+\.\S+$')] = ...,
    user_controller: UserController = Depends(get_user_controller)
):
    try:
        return user_controller.delete(email)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))