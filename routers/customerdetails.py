import fastapi
from fastapi import FastAPI,APIRouter,Depends,status,Request,Form
from sqlalchemy.orm import Session
from . import get_db
from routers.models import ItemDetails,CustomerDetails
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import or_
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

class items(BaseModel):
    item_id : str
    item_name : str
    price : str

@router.get('/customers',response_class=HTMLResponse)
def form(request:Request,db: Session = Depends(get_db)):
    all_customers = db.query(CustomerDetails).all()
    return templates.TemplateResponse("/customers.html",{"request":request,"customers":all_customers})

@router.post('/createCustomer')
async def create_customer(customer_id: str = Form(...), name: str = Form(...), address: str = Form(...),phone_no: int = Form(...),whatsapp_no: int = Form(...) ,db: Session = Depends(get_db)):
    item_details = db.query(CustomerDetails).filter(CustomerDetails.customer_id == customer_id).first()
    if item_details:
        return {"message": "Customer with same Customer id already exists"}
    else:
        db_item = CustomerDetails(
            customer_id=customer_id,
            name=name,
            address=address,
            phone_no=str(phone_no),
            whatsapp_no=str(whatsapp_no)
        )
        db.add(db_item)
        db.commit()
        response = RedirectResponse(url='/customers', status_code=status.HTTP_302_FOUND)
        return response
    
@router.post('/editCustomer')
async def edit_order(customer_id: str = Form(...),
                     name: str = Form(...),
                     address: str = Form(...),
                     phone_no: str = Form(...),
                     whatsapp_no: int = Form(...),
                     db: Session = Depends(get_db)):
    order = db.query(CustomerDetails).filter_by(customer_id=customer_id).first()
    order.customer_id = customer_id
    order.name = name
    order.address = address
    order.whatsapp_no = whatsapp_no
    order.phone_no = phone_no
    db.commit()
    response = RedirectResponse(url='/customers', status_code=status.HTTP_302_FOUND)
    return response

@router.post('/deleteCustomer')
async def delete_order(customer_id: str = Form(...), db: Session = Depends(get_db)):
    order = db.query(CustomerDetails).filter_by(customer_id=customer_id).first()
    db.delete(order)
    db.commit()
    response = RedirectResponse(url='/customers', status_code=status.HTTP_302_FOUND)
    return response