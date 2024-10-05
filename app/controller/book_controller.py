from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.model.book import Book as BookModel
from app.database.schema import Book as BookSchema


class BookController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, book: BookSchema):
        if existing_book := self.get(book.isbn):
            raise HTTPException(status_code=409, detail="Book already registered")
        
        book = BookModel(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            publish_year=book.publish_year
        )

        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)

        return {"success": True, "detail": "Book created successfully"}  

    def get(self, isbn: str):
        book = self.db.query(BookModel).filter(BookModel.isbn == isbn).first()
        return book

    def get_all(self):
        books = self.db.query(BookModel).order_by(BookModel.publish_year.asc()).all()
        books_list = [
            {
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "publish_year": book.publish_year
            }
            for book in books
        ]
        return books_list

    def update(self, book: BookSchema):
        if existing_book := self.get(book.isbn):
            existing_book.title = book.title
            existing_book.author = book.author
            existing_book.publish_year = book.publish_year

            try:
                self.db.commit()
                return {"success": True, "detail": "Book updated successfully"}
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Error updating book, {e}")
        else:
            raise HTTPException(status_code=404, detail="Book not found")

    def delete(self, book: BookSchema):
        if existing_book := self.get(book.isbn):
            try:
                self.db.delete(existing_book)
                self.db.commit()
                return {"success": True, "detail": "Book deleted successfully"}
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Error deleting book, {e}")
        else:
            raise HTTPException(status_code=404, detail="Book not found")
