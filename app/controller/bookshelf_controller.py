import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.model.bookshelf import Bookshelf
from app.database.schema import Bookshelf as BookshelfSchema
from app.model.book import Book
from app.util.constants import ALPHABET_TITLE, ALPHABET_AUTHOR


class BookshelfController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_to_shelf(self, bookshelf: BookshelfSchema):
        if book_on_shelf := self.check_if_book_on_shelf(bookshelf):
            raise HTTPException(status_code=409, detail="Book already on shelf")
        
        bookshelf = Bookshelf(
            book_isbn=bookshelf.book_isbn,
            user_email=bookshelf.user_email
        )

        try:
            self.db.add(bookshelf)
            self.db.commit()
            self.db.refresh(bookshelf)

            return {"success": True, "detail": "Book added to shelf"}
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def check_if_book_on_shelf(self, bookshelf: BookshelfSchema):
        try:
            return self.db.execute(
                select(Bookshelf)
                .filter(Bookshelf.book_isbn == bookshelf.book_isbn)
                .filter(Bookshelf.user_email == bookshelf.user_email)
            ).scalar()
        except Exception as e:
            logging.error(f"Error on get, exc: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def retrieve_bookshelf(self, user_email: str, filter: int):
        try:
            if not filter: # chronological order
                bookshelf = (
                    self.db.query(Book)
                    .join(Bookshelf, Book.isbn == Bookshelf.book_isbn)
                    .filter(Bookshelf.user_email == user_email)
                    .order_by(Book.publish_year.asc())
                )

            if filter and filter == ALPHABET_TITLE:
                bookshelf = (
                    self.db.query(Book)
                    .join(Bookshelf, Book.isbn == Bookshelf.book_isbn)
                    .filter(Bookshelf.user_email == user_email)
                    .order_by(Book.title.asc())
                )

            if filter and filter == ALPHABET_AUTHOR:
                bookshelf = (
                    self.db.query(Book)
                    .join(Bookshelf, Book.isbn == Bookshelf.book_isbn)
                    .filter(Bookshelf.user_email == user_email)
                    .order_by(Book.author.asc())
                )

            return bookshelf
        except Exception as e:
            logging.error(f"Error on get, exc: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def remove_from_shelf(self, bookshelf: BookshelfSchema):
        if book_on_shelf := self.check_if_book_on_shelf(bookshelf):
            try:
                self.db.delete(book_on_shelf)
                self.db.commit()
                return {"success": True, "detail": "Book removed from shelf"}
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Error removing book, {e}")
        else:
            raise HTTPException(status_code=404, detail="Book not on shelf")
