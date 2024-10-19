import logging

import bcrypt
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.schema import User as UserSchema
from app.model.user import User as UserModel


class UserController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user: UserSchema):
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        
        user = UserModel(
            name=user.name,
            email=user.email,
            password=hashed_password.decode('utf-8')
        )

        try:
            self.db.add(user)
            self.db.commit()

            return JSONResponse(
                content={"success": True, "detail": "User created successfully"},
                status_code=201
            )
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User already registered")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get(self, email: str):
        try:
            return self.db.execute(
                select(UserModel).filter(UserModel.email == email)
            ).scalar()
        except Exception as e:
            logging.error(f"Error on get, exc: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_all(self):
        try:
            return self.db.query(UserModel)
        except Exception as e:
            logging.error(f"Error on get, exc: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update(self, user: UserSchema):
        if existing_user := self.get(user.email):
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

            existing_user.name = user.name
            existing_user.password = hashed_password.decode('utf-8')
            try:
                self.db.commit()
                return JSONResponse(
                    content={"success": True, "detail": "User updated successfully"},
                    status_code=200
                )
            except Exception as e:
                self.db.rollback()
                logging.error(f"Error on update, exc: {e}")
                raise HTTPException(status_code=500, detail=f"Error updating user, {e}")
        else:
            raise HTTPException(status_code=404, detail="User not found")

    def delete(self, email: str):
        if existing_user := self.get(email):
            try:
                self.db.delete(existing_user)
                self.db.commit()
                return JSONResponse(
                    content={"success": True, "detail": "User deleted successfully"},
                    status_code=200
                )
            except Exception as e:
                self.db.rollback()
                logging.error(f"Error on delete, exc: {e}")
                raise HTTPException(status_code=500, detail="Internal Server Error")
        else:
            raise HTTPException(status_code=404, detail="User not found")
