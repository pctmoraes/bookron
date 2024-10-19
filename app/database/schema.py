from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=3)
    email: str = Field(pattern=r'^\S+@\S+\.\S+$')
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    name: str = Field(min_length=3)
    email: str = Field(pattern=r'^\S+@\S+\.\S+$')

class Book(BaseModel):
    isbn: str = Field(min_length=13)
    title: str = Field(min_length=1)
    author: str = Field(min_length=3)
    publish_year: int = Field(default=0)
    genre: str = Field(min_length=3)

class Bookshelf(BaseModel):
    book_isbn: str = Field(min_length=13)
    user_email: str = Field(pattern=r'^\S+@\S+\.\S+$')

class ErrorResponse(BaseModel):
    detail: str
