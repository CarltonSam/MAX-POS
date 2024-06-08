import fastapi
from fastapi import FastAPI,APIRouter,Depends,status,Request,Form
from sqlalchemy.orm import Session
from . import get_db
from routers.models import ItemDetails,CustomerDetails,OrderItems,OrderDetails
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import or_
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Body
from typing import List, Dict
import json
from datetime import date
from sqlalchemy import func


templates = Jinja2Templates(directory="templates")

router = APIRouter()

class CartItem(BaseModel):
    itemId: str
    itemName: str
    price: float
    quantity: int

class items(BaseModel):
    item_id : str
    item_name : str
    price : str

@router.get('/orders',response_class=HTMLResponse)
def form(request:Request,db: Session = Depends(get_db)):
    all_items = db.query(ItemDetails).all()
    all_customers = db.query(CustomerDetails).all()
    return templates.TemplateResponse("/yrdy.html",{"request":request,"items":all_items,"customers":all_customers})

@router.post('/checkout')
def cart(date: str = Form(...),order_id: str = Form(...),customer_id: str = Form(...),cartData: List = Form(...),db: Session = Depends(get_db)):
    data=cartData[0]
    list_of_dicts = json.loads(data)
    for item in list_of_dicts:
        total_price=int(float(item['quantity'])*float(item['price']))
        db_item = OrderItems(
            order_id=order_id,
            customer_id=customer_id,
            item_id=item['itemId'],
            item_name=item['itemName'],
            item_quantity=int(float(item['quantity'])),
            item_price=int(float(item['price'])),
            total_price=total_price
            )
        db.add(db_item)
        db.commit()
    customer = db.query(CustomerDetails).filter_by(customer_id=customer_id).first()
    total_quantity = db.query(func.sum(OrderItems.item_quantity)).filter_by(order_id=order_id).scalar()
    total_price = db.query(func.sum(OrderItems.total_price)).filter_by(order_id=order_id).scalar()
    

    db_orderdetails = OrderDetails(
        order_id=order_id,
        date=date,
        customer_id=customer_id,
        cust_name=customer.name,
        total_items=total_quantity,
        status='RECEIVED',
        due = total_price
        )
    db.add(db_orderdetails)
    db.commit()

    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)