import os
from dotenv import load_dotenv

load_dotenv()

USER = os.environ.get('DATABASE_USER')
PASSWORD = os.environ.get('DATABASE_PASS')
DB = os.environ.get('DATABASE_NAME')
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@localhost/{DB}"

OPENAPI_KEY = os.environ.get('OPENAPI_KEY')

CHRONOLOGICAL = 0
ALPHABET_TITLE = 1
ALPHABET_AUTHOR = 2