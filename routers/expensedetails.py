from datetime import date
from typing import Optional
import fastapi
from fastapi import FastAPI,APIRouter,Depends, Query,status,Request,Form
from openpyxl import Workbook
from sqlalchemy.orm import Session
from . import get_db
from routers.models import Expenses,Cashbook
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import or_
from fastapi.responses import FileResponse, HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()
def generate_excel_file(data):
    wb = Workbook()
    ws = wb.active

    # Add table headers
    headers = ["Date", "Expense Head", "Expense Name", "Amount"]
    ws.append(headers)

    # Add table data
    for item in data:
        row = [item.date, item.expense_head, item.expense_name, item.expense_amount]
        ws.append(row)

    # Save the workbook
    filename = "expense_data.xlsx"
    wb.save(filename)

    return filename

@router.get("/expenses/download", response_class=FileResponse)
def download_cashbook_data(from_date: Optional[str] = Query(None, alias="from_date"), till_date: Optional[str] = Query(None, alias="till_date"), db: Session = Depends(get_db)):
    query = db.query(Expenses)

    if from_date:
        query = query.filter(Expenses.date >= from_date)
    if till_date:
        query = query.filter(Expenses.date <= till_date)

    cashbook_data = query.all()
    filename = generate_excel_file(cashbook_data)

    return filename

@router.get('/expenses',response_class=HTMLResponse,include_in_schema=False)
def form(request:Request,from_date: Optional[str] = None, till_date: Optional[str] = None,db: Session = Depends(get_db)):
    all_items = db.query(Expenses).all()
    query = db.query(Expenses)

    if from_date:
        query = query.filter(Expenses.date >= from_date)
    if till_date:
        query = query.filter(Expenses.date <= till_date)

    total_price = sum(order.expense_amount for order in query)
    return templates.TemplateResponse("/expenses.html",{"request":request,"expenses":all_items,'total_price':total_price})

@router.post('/createExpense')
async def create_customer(expense_head: Optional[str] = Form(...),expense_name: str = Form(...), date: str = Form(...), expense_amount: int = Form(...), db: Session = Depends(get_db)):
    db_item = Expenses(
            expense_head=expense_head,
            expense_name=expense_name,
            date=date,
            expense_amount=expense_amount
    )
    cashbook_expense = Cashbook(
        date = date,
            category = expense_head,
            text = expense_name,
            credit = expense_amount
        
    )
    db.add(cashbook_expense)
    db.add(db_item)
    db.commit()
    response = RedirectResponse(url='/expenses', status_code=status.HTTP_302_FOUND)
    return response

@router.post('/deleteExpense')
async def delete_expense(date: str = Form(...), expense_name: str = Form(...), expense_head: str = Form(...), expense_amount: str = Form(...), db: Session = Depends(get_db)):
    expense = db.query(Expenses).filter(
        Expenses.date == date,
        Expenses.expense_name == expense_name,
        Expenses.expense_head == expense_head,
        Expenses.expense_amount == int(expense_amount)
    ).first()

    cashbook = db.query(Cashbook).filter(
        Cashbook.date == date,
        Cashbook.category == expense_head,
        Cashbook.text == expense_name,
        Cashbook.credit == int(expense_amount)
    ).first()

    if expense:
        db.delete(expense)
        db.commit()

    if cashbook:
        db.delete(cashbook)
        db.commit()

    response = RedirectResponse(url='/expenses', status_code=status.HTTP_302_FOUND)
    return response

