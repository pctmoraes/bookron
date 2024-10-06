from fastapi import FastAPI
from app.view.user_view import route as user
from app.view.book_view import route as book
from app.view.bookshelf_view import route as bookshelf

app = FastAPI()

@app.get('/')
def main():
    return 'hello, this is the home page of BooKron!'

app.include_router(user)
app.include_router(book)
app.include_router(bookshelf)