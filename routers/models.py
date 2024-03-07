from fastapi import FastAPI,APIRouter
from . import get_db

from sqlalchemy import ARRAY, Date, Integer, PrimaryKeyConstraint, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from . import engine

Base = declarative_base()

class UserDetails(Base):
    __tablename__ = "users"

    email = Column(String,primary_key=True,index=True)
    hashed_password = Column(String)

