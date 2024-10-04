import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.model.user import User as UserModel
from app.database.schema import User as UserSchema


class UserController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user: UserSchema):
        if existing_user := self.get(user.email):
            raise HTTPException(status_code=409, detail="User already registered")

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        
        user = UserModel(
            name=user.name,
            email=user.email,
            password=hashed_password.decode('utf-8')
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return {"success": True, "detail": "User created successfully"}
        

    def get(self, email: str):
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return user
