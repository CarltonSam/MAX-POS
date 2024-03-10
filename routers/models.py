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

class CustomerDetails(Base):
    __tablename__ = "customers"

    customer_id = Column(String,primary_key=True,index=True)
    name = Column(String)
    address = Column(String)
    phone_no = Column(Integer)
    whatsapp_no = Column(Integer)

class ItemDetails(Base):
    __tablename__ = "itemprice"

    item_id = Column(String,primary_key=True,index=True)
    item_name = Column(String)
    price = Column(Integer)

class OrderDetails(Base):
    __tablename__ = "orders"

    order_id = Column(String,primary_key=True,index=True)
    date = Column(Date)
    customer_id = Column(String)
    cust_name = Column(String)
    total_items = Column(Integer)
    status = Column(String)
    ready_date = Column(Date)
    delivery_date = Column(Date)
    cash = Column(Integer)
    bank = Column(Integer)
    advance_paid = Column(Integer)
    due = Column(Integer)

class OrderItems(Base):
    __tablename__ = "orderitems"

    order_id = Column(String)
    customer_id = Column(String)
    item_id = Column(String)
    item_name = Column(String)
    item_quantity = Column(Integer)
    item_price = Column(Integer)
    total_price = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'item_id'),
    )


Base.metadata.create_all(bind=engine)
