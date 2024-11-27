import logging

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.schema import Book as BookSchema
from app.model.book import Book as BookModel
from app.util.constants import OPENAPI_KEY


class BookController:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, book: BookSchema):
        publish_year = book.publish_year
        genre = book.genre

        if not publish_year or not genre:
            publish_year = self.get_publish_year_and_genre_with_AI(book)
        
        book = BookModel(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            publish_year=publish_year,
            genre=genre
        )

        try:
            self.db.add(book)
            self.db.commit()

            return JSONResponse(
                content={"success": True, "detail": "Book created successfully"},
                status_code=201
            )
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Book already registered")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error") 

    def get(self, isbn: str):
        try:
            return self.db.execute(
                select(BookModel).filter(BookModel.isbn == isbn)
            ).scalar()
        except Exception as e:
            logging.error(f"Error on get, exc: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_all(self):
        try:
            return self.db.query(BookModel)
        except Exception as e:
            logging.error(f"Error on get, exc: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update(self, book: BookSchema):
        if existing_book := self.get(book.isbn):
            existing_book.title = book.title
            existing_book.author = book.author
            existing_book.publish_year = book.publish_year
            existing_book.genre = book.genre

            try:
                self.db.commit()
                return JSONResponse(
                    content={"success": True, "detail": "Book updated successfully"},
                    status_code=200
                )
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Error updating book, {e}")
        else:
            raise HTTPException(status_code=404, detail="Book not found")

    def delete(self, isbn: str):
        if existing_book := self.get(isbn):
            try:
                self.db.delete(existing_book)
                self.db.commit()
                return JSONResponse(
                    content={"success": True, "detail": "Book deleted successfully"},
                    status_code=200
                )
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Error deleting book, {e}")
        else:
            raise HTTPException(status_code=404, detail="Book not found")

    def get_publish_year_and_genre_with_AI(self, book: BookSchema):
        openai = OpenAI(api_key=OPENAPI_KEY)
        publish_year, genre = 0, ""

        question = "Return me in this format publish_year,book_genre " \
            "(e.g the year a comma and the genre) with no additional data " \
            f"the publish year and genre of the book {book.title} by author {book.author} " \
            "and in Brazilian portuguese"
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a book expert."},
                    {"role": "user", "content": question}
                ]
            )

            anwswers = response['choices'][0]['message']['content']
            anwswers_list = anwswers.split(',')
            
            anwswer_publish_year = anwswers_list[0]
            if anwswer_publish_year and anwswer_publish_year.isdecimal():
                publish_year = int(anwswer_publish_year)
            
            anwswer_genre = anwswers_list[-1]
            genre = "N/A" if not anwswer_genre else anwswer_genre.capitalize()
        except Exception as e:
            logging.error(
                f'An exception occurred during openai.chat.completions.create() call. ' \
                f'Traceback: {e}'
            )
        finally:
            return publish_year, genre
