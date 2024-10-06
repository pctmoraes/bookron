from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.model.bookshelf import Bookshelf
from app.database.schema import Bookshelf as BookshelfSchema
from app.model.book import Book


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

        self.db.add(bookshelf)
        self.db.commit()
        self.db.refresh(bookshelf)

        return {"success": True, "detail": "Book added to shelf"}  

    def check_if_book_on_shelf(self, bookshelf: BookshelfSchema):
        book = self.db.query(Bookshelf) \
            .filter(Bookshelf.book_isbn == bookshelf.book_isbn) \
            .filter(Bookshelf.user_email == bookshelf.user_email).first()

        return book

    def retrieve_bookshelf(self, user_email: str, filter: int):
        bookshelf = self.db.query(Book) \
            .join(Bookshelf, Book.isbn == Bookshelf.book_isbn) \
            .filter(Bookshelf.user_email == user_email)
        
        if not filter:
            bookshelf.order_by(Book.publish_year.asc()).all()
        
        if filter and filter == 1:
            bookshelf.order_by(Book.title.asc()).all()

        if filter and filter == 2:
            bookshelf.order_by(Book.author.asc()).all()

        books = [
            {
                "title": book.title,
                "author": book.author,
                "publish_year": book.publish_year
            }
            for book in bookshelf
        ]

        return books

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

