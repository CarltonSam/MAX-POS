from fastapi import FastAPI,APIRouter,Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import get_db
from routers.models import CustomerDetails
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = APIRouter()

class customer(BaseModel):
    customer_id : str
    name : str
    address : str
    phone_no : int
    whatsapp_no : int

@router.post("/createCustomer")
async def create_customer(details:customer,db: Session = Depends(get_db)):
    cust_details=db.query(CustomerDetails).filter(CustomerDetails.customer_id == details.customer_id).first()
    if cust_details:
        return {"message" : "customer with same customer id already exists"}
    else:
        db_customer = CustomerDetails(
            customer_id = details.customer_id,
            name = details.name,
            address = details.address,
            phone_no = details.phone_no,
            whatsapp_no = details.whatsapp_no
            )
    db.add(db_customer)
    db.commit()
    return {"message" : "Customer Details Added!"}