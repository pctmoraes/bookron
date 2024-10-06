from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'bookron'}
    
    name = Column(String(256), nullable=False)
    email = Column(String(50), primary_key=True)
    password = Column(String(500), nullable=False)
