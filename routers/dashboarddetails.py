import fastapi
from fastapi import FastAPI,APIRouter,Depends,status,Request,Form,Body
from sqlalchemy.orm import Session
from . import get_db
from routers.models import OrderDetails,ItemDetails, OrderItems
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import func, or_
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

templates = Jinja2Templates(directory="templates")

router = APIRouter()

class OrderEdit(BaseModel):
    order_id: str
    date: str
    customer_id: str
    cust_name: str
    total_items: int
    status: str
    ready_date: str
    delivery_date: str
    cash: float
    bank: str
    advance_paid: float
    due: float

@router.get('/dashboard',response_class=HTMLResponse,include_in_schema=False)
def form(request: Request, db: Session = Depends(get_db)):
    orderItems = db.query(OrderItems).all()
    orders = db.query(OrderDetails).all()
    ready=db.query(OrderDetails).filter_by(status="READY").all()
    delivered=db.query(OrderDetails).filter_by(status="DELIVERED").all()
    print(orderItems)
    return templates.TemplateResponse("/dashboard.html", {"request": request, "orders": orders, "orderItems": orderItems,"ordered":len(orders),"ready":len(ready),"delivered":len(delivered)})

@router.post('/editOrder')
async def edit_order(order_id: str = Form(...),
    date: str = Form(...),
    customer_id: str = Form(...),
    cust_name: str = Form(...),
    total_items: int = Form(...),
    order_status: str = Form(...),
    ready_date: Optional[str] = Form(None),
    delivery_date: Optional[str] = Form(None),
    cash: str = Form(...),
    bank: str = Form(...),
    advance_paid: str = Form(...),
    due: str = Form(...),db:Session=Depends(get_db)):
        total_price = db.query(func.sum(OrderItems.total_price)).filter_by(order_id=order_id).scalar()
        order=db.query(OrderDetails).filter_by(order_id=order_id).first()
        order.order_id=order_id
        order.date=date
        order.customer_id=customer_id
        order.cust_name=cust_name
        order.total_items=total_items
        order.status=order_status
        order.ready_date = ready_date if ready_date else None  # Assign None if ready_date is None or empty string
        order.delivery_date = delivery_date if delivery_date else None
        order.cash=cash
        order.bank=bank
        order.advance_paid=advance_paid
        order.due=int(total_price)-int(order.bank)-int(order.advance_paid)
        db.commit()
        response = RedirectResponse(url='/dashboard', status_code=status.HTTP_302_FOUND)
        return response