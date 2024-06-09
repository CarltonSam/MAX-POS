from fastapi import FastAPI, APIRouter, Depends, Query, status, Request, Form
from openpyxl import Workbook
from sqlalchemy.orm import Session
from . import get_db
from routers.models import OrderDetails, OrderItems,Cashbook
from sqlalchemy import func
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from datetime import date
from pydantic import BaseModel

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
    
def generate_excel_file(data):
    wb = Workbook()
    ws = wb.active

    # Add table headers
    headers = ["Order ID", "Date", "Customer ID", "Customer Name","Total Items", "Status", "Ready Date", "Delivery Date","Note", "Cash", "Advance Paid", "Due"]
    ws.append(headers)

    # Add table data
    for item in data:
        row = [item.order_id, item.date, item.customer_id, item.cust_name, item.total_items, item.status, item.ready_date, item.delivery_date, item.note, item.cash, item.advance_paid, item.due]
        ws.append(row)

    # Save the workbook
    filename = "dashboard_data.xlsx"
    wb.save(filename)

    return filename

@router.get("/dashboard/download", response_class=FileResponse)
def download_cashbook_data(from_date: Optional[str] = Query(None, alias="from_date"), 
                           till_date: Optional[str] = Query(None, alias="till_date"), 
                           status: Optional[str] = Query(None, alias="status"), 
                           db: Session = Depends(get_db)):

    query = db.query(OrderDetails)

    if from_date:
        query = query.filter(OrderDetails.date >= from_date)
    if till_date:
        query = query.filter(OrderDetails.date <= till_date)
    if status:
        query = query.filter(OrderDetails.status == status)

    cashbook_data = query.all()
    filename = generate_excel_file(cashbook_data)

    return filename

@router.get('/dashboard', response_class=HTMLResponse, include_in_schema=False)
def dashboard(request: Request, from_date: Optional[str] = None, till_date: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(OrderDetails)

    if from_date:
        query = query.filter(OrderDetails.date >= from_date)
    if till_date:
        query = query.filter(OrderDetails.date <= till_date)
    if status:
        query = query.filter(OrderDetails.status == status)

    orders = query.all()
    received = db.query(OrderDetails).filter_by(status="RECEIVED").all()
    ready = db.query(OrderDetails).filter_by(status="READY").all()
    delivered = db.query(OrderDetails).filter_by(status="DELIVERED").all()

    total_items = sum(order.total_items for order in orders)
    total_price = sum(order.due for order in orders)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "orders": orders,
        "ordered": len(received),
        "ready": len(ready),
        "delivered": len(delivered),
        "total_items": total_items,
        "total_price": total_price
    })

@router.post('/editOrder')
async def edit_order(order_id: str = Form(...),
                     order_date: str = Form(...),
                     customer_id: str = Form(...),
                     cust_name: str = Form(...),
                     total_items: int = Form(...),
                     order_status: str = Form(...),
                     ready_date: Optional[str] = Form(None),
                     delivery_date: Optional[str] = Form(None),
                     cash: Optional[str] = Form(...),
                     note: Optional[str] = Form(None),
                     advance_paid: str = Form(...),
                     due: str = Form(...),
                     db: Session = Depends(get_db)):
    total_price = db.query(func.sum(OrderItems.total_price)).filter_by(order_id=order_id).scalar()
    order = db.query(OrderDetails).filter_by(order_id=order_id).first()
    order.order_id = order_id
    order.date = order_date
    order.customer_id = customer_id
    order.cust_name = cust_name
    order.total_items = total_items
    order.status = order_status
    order.ready_date = ready_date if ready_date else None
    order.delivery_date = delivery_date if delivery_date else None
    if int(order.cash) != int(cash):
        cashbook_entry = Cashbook(
            date = date.today(),
            category = order_id,
            text = note,
            debit = cash
        )
        order.cash = cash
        db.add(cashbook_entry)
    order.note = note
    if int(order.advance_paid) != int(advance_paid):
        cashbook_entry = Cashbook(
            date = date.today(),
            category = order_id,
            text = note,
            debit = advance_paid
        )
        order.advance_paid = advance_paid
        db.add(cashbook_entry)
    order.due = int(total_price) - int(order.cash) - int(order.advance_paid)
    db.commit()
    response = RedirectResponse(url='/dashboard', status_code=status.HTTP_302_FOUND)
    return response

@router.post('/deleteOrder')
async def delete_order(order_id: str = Form(...), db: Session = Depends(get_db)):
    order = db.query(OrderDetails).filter_by(order_id=order_id).first()
    order_items=db.query(OrderItems).filter_by(order_id=order_id).all()
    if order:
        db.delete(order)

    for item in order_items:
        db.delete(item)

    db.commit()
    response = RedirectResponse(url='/dashboard', status_code=status.HTTP_302_FOUND)
    return response
