from fastapi import FastAPI,APIRouter
from . import get_db

from sqlalchemy import ARRAY, Date, Integer, PrimaryKeyConstraint, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from . import engine

Base = declarative_base()

class UserDetails(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'max'}

    email = Column(String,primary_key=True,index=True)
    hashed_password = Column(String)

class CustomerDetails(Base):
    __tablename__ = "customers"
    __table_args__ = {'schema': 'max'}

    customer_id = Column(String,primary_key=True,index=True)
    name = Column(String)
    address = Column(String)
    phone_no = Column(String)
    whatsapp_no = Column(String)

class ItemDetails(Base):
    __tablename__ = "itemprice"
    __table_args__ = {'schema': 'max'}

    item_id = Column(String,primary_key=True,index=True)
    item_name = Column(String)
    price = Column(Integer)

class OrderDetails(Base):
    __tablename__ = "orders"
    __table_args__ = {'schema': 'max'}

    order_id = Column(String, primary_key=True, index=True)
    note = Column(String,default="")
    date = Column(Date)
    customer_id = Column(String)
    cust_name = Column(String)
    total_items = Column(Integer, default=0)  # Default value for total_items
    status = Column(String)
    ready_date = Column(String)
    delivery_date = Column(String)
    cash = Column(Integer, default=0)  # Default value for cash
    advance_paid = Column(Integer, default=0)  # Default value for advance_paid
    due = Column(Integer, default=0)  # Default value for due

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
        {'schema': 'max'}
    )

class Expenses(Base):
    __tablename__ = "expenses"
    __table_args__ = {'schema': 'max'}

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    date = Column(Date)
    expense_head = Column(String)
    expense_name = Column(String)
    expense_amount = Column(Integer)

class Cashbook(Base):
    __tablename__ = "cashbook"
    __table_args__ = {'schema': 'max'}

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    date = Column(Date)
    category = Column(String)
    text = Column(String)
    credit = Column(Integer,default=0)
    debit = Column(Integer,default=0)
    balance = Column(Integer,default=0)


Base.metadata.create_all(bind=engine)
