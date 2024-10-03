from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def main():
    return 'hello, this is the home page of BooKron!'
