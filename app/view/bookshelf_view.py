from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from sqlalchemy.orm import Session
from app.database.schema import Bookshelf, ErrorResponse
from app.controller.bookshelf_controller import BookshelfController
from app.database.database import get_db

route = APIRouter(prefix='/bookshelf')

def get_bookshelf_controller(db: Session = Depends(get_db)) -> BookshelfController:
    return BookshelfController(db)

@route.post('/add_to_shelf', responses={500: {"model": ErrorResponse}})
def add_to_shelf(
    bookshelf: Annotated[Bookshelf, Query()] = ...,
    book_controller: BookshelfController = Depends(get_bookshelf_controller)
):
    try:
        return book_controller.add_to_shelf(bookshelf)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.get('/books', responses={500: {"model": ErrorResponse}})
def retrieve_bookshelf(
    user_email: Annotated[str, Query()] = ...,
    filter: Annotated[int, None] = None,
    bookshelf_controller: BookshelfController = Depends(get_bookshelf_controller)
):
    try:
        shelf = bookshelf_controller.retrieve_bookshelf(user_email, filter)
        return {"success": True, "books": shelf}
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@route.delete('/delete', responses={500: {"model": ErrorResponse}})
def delete(
    bookshelf: Annotated[Bookshelf, Query()] = ...,
    book_controller: BookshelfController = Depends(get_bookshelf_controller)
):
    try:
        return book_controller.remove_from_shelf(bookshelf)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(400, detail=str(e))