from typing import Optional
import fastapi
from fastapi import FastAPI,APIRouter,Depends, Query,status,Request,Form
from sqlalchemy.orm import Session
from . import get_db
from routers.models import Cashbook
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import or_
from fastapi.responses import FileResponse, HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from openpyxl import Workbook

def generate_excel_file(data):
    wb = Workbook()
    ws = wb.active

    # Add table headers
    headers = ["Date", "Category", "Text", "Debit", "Credit"]
    ws.append(headers)

    # Add table data
    for item in data:
        row = [item.date, item.category, item.text, item.debit, item.credit]
        ws.append(row)

    # Save the workbook
    filename = "cashbook_data.xlsx"
    wb.save(filename)

    return filename

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/cashbook/download", response_class=FileResponse)
def download_cashbook_data(from_date: Optional[str] = Query(None, alias="from_date"), till_date: Optional[str] = Query(None, alias="till_date"), db: Session = Depends(get_db)):
    query = db.query(Cashbook)

    if from_date:
        query = query.filter(Cashbook.date >= from_date)
    if till_date:
        query = query.filter(Cashbook.date <= till_date)

    cashbook_data = query.all()
    filename = generate_excel_file(cashbook_data)

    return filename



@router.get('/cashbook',response_class=HTMLResponse,include_in_schema=False)
def form(request:Request,from_date: Optional[str] = None, till_date: Optional[str] = None,db: Session = Depends(get_db)):
    query = db.query(Cashbook)

    if from_date:
        query = query.filter(Cashbook.date >= from_date)
    if till_date:
        query = query.filter(Cashbook.date <= till_date)

    orders = query.order_by(Cashbook.id).all()
    total_debit = sum(order.debit or 0 for order in orders if order.credit is not None)
    total_credit = sum(order.credit or 0 for order in orders if order.debit is not None)
    total_price = sum(order.debit or 0 for order in orders if order.credit is not None) - sum(order.credit or 0 for order in orders if order.debit is not None)

    return templates.TemplateResponse("/cashbook.html",{"request":request,"cashbook":orders,"total_price":total_price,"total_debit":total_debit,"total_credit":total_credit})