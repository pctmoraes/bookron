import os
from dotenv import load_dotenv

load_dotenv()

USER = os.environ.get('DATABASE_USER')
PASSWORD = os.environ.get('DATABASE_PASS')
DB = os.environ.get('DATABASE_NAME')

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@localhost/{DB}"