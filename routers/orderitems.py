from datetime import date
from typing import Optional
import fastapi
from fastapi import FastAPI,APIRouter,Depends,status,Request,Form
from sqlalchemy.orm import Session
from . import get_db
from routers.models import Expenses,Cashbook,OrderItems
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import or_
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get('/orderitems',response_class=HTMLResponse,include_in_schema=False)
def form(request:Request,db: Session = Depends(get_db)):
    all_items = db.query(OrderItems).all()
    return templates.TemplateResponse("/orderitems.html",{"request":request,"orders":all_items})