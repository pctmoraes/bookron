from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from sqlalchemy.orm import Session
from app.database.schema import Book
from app.controller.book_controller import BookController
from app.database.database import get_db

route = APIRouter(prefix='/book')

def get_book_controller(db: Session = Depends(get_db)) -> BookController:
    return BookController(db)

@route.post('/create')
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

@route.get('/{isbn}')
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

@route.get('/books/list')
def get_all(
    book_controller: BookController = Depends(get_book_controller)
):
    try:
        books = book_controller.get_all()
        return {"success": True, "books": books}
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.put('/update')
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

@route.delete('/delete')
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