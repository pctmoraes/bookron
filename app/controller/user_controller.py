import bcrypt
from sqlalchemy.orm import Session
from app.model.user import User as UserModel
from app.database.schema import User as UserSchema


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

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get(self, email: str):
        user_obj = self.db.query(UserModel).filter(UserModel.email == email).first()

        if user_obj:
            return {"success": True, "detail": user_obj.name}

        return {"success": False, "detail": "User not found"}
