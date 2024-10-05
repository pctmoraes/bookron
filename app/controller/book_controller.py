import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from openai import OpenAI
from app.model.book import Book as BookModel
from app.database.schema import Book as BookSchema
from app.util.constants import OPENAPI_KEY


class BookController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, book: BookSchema):
        if existing_book := self.get(book.isbn):
            raise HTTPException(status_code=409, detail="Book already registered")
        
        publish_year = book.publish_year
        if not publish_year:
            publish_year = self.get_publish_year_with_AI(book)
        
        book = BookModel(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            publish_year=publish_year
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

    def get_publish_year_with_AI(self, book: BookSchema):
        openai = OpenAI(api_key=OPENAPI_KEY)
        publish_year = 0
        question = f"When was '{book.title}' by {book.author} published? " \
            "Please return me only the year, no phrases."
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a book expert."},
                    {"role": "user", "content": question}
                ]
            )

            content = response['choices'][0]['message']['content']
            if content and content.isdecimal():
                publish_year = int(content)
        
        except Exception as e:
            logging.error(
                f'An exception occurred during openai.chat.completions.create() call. ' \
                f'Traceback: {e}'
            )
        finally:
            return publish_year
