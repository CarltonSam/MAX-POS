from fastapi import FastAPI,APIRouter,Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import get_db
from routers.models import UserDetails
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class user(BaseModel):
    email:str
    password:str

@router.post("/login")
async def login(details:user,db: Session = Depends(get_db)):
    user_details=db.query(UserDetails).filter(UserDetails.email == details.email, UserDetails.hashed_password == details.password).first()
    if user_details:
        return {"message : login successful"}
    else:
        return {"message : login failed"}
    
