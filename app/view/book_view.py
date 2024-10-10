from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from app.database.schema import Book, ErrorResponse
from app.controller.book_controller import BookController
from app.database.database import get_db

route = APIRouter(prefix='/book')

def get_book_controller(db: Session = Depends(get_db)) -> BookController:
    return BookController(db)

@route.post('/create', responses={500: {"model": ErrorResponse}})
def create(
    book: Annotated[Book, Query()],
    book_controller: BookController = Depends(get_book_controller)
):
    try:
        return book_controller.create(book)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.get('/{isbn}', responses={500: {"model": ErrorResponse}})
def get(
    isbn: str = Path(regex=r'^\S+@\S+\.\S+$'),
    book_controller: BookController = Depends(get_book_controller)
):
    try:
        if book := book_controller.get(isbn):
            return {"success": True, "book title": book.title}
        raise HTTPException(404, detail="Book not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.get('/books/list', response_model=Page[Book], responses={500: {"model": ErrorResponse}})
def get_all(
    book_controller: BookController = Depends(get_book_controller)
):
    try:
        books = book_controller.get_all()
        return paginate(books)
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.put('/update', responses={500: {"model": ErrorResponse}})
def update(
    book: Annotated[Book, Query()] = ...,
    book_controller: BookController = Depends(get_book_controller)
):
    try:
        return book_controller.update(book)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.delete('/delete', responses={500: {"model": ErrorResponse}})
def delete(
    isbn: Annotated[str, Query(min_length=13)] = ...,
    book_controller: BookController = Depends(get_book_controller)
):
    try:
        return book_controller.delete(isbn)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))