from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=3)
    email: str = Field(pattern=r'^\S+@\S+\.\S+$')
    password: str = Field(min_length=6)
