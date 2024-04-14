import fastapi
from fastapi import FastAPI, APIRouter, Depends, Request,status,Form
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import get_db
from routers.models import UserDetails
from pydantic import BaseModel
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    email: str
    password: str

@router.get('/',response_class=HTMLResponse,include_in_schema=False)
def form(request:Request):
    return templates.TemplateResponse("/index.html",{"request":request})


@router.post("/",response_class=HTMLResponse)
async def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_details = db.query(UserDetails).filter(UserDetails.email == email, UserDetails.hashed_password == password).first()
    if user_details:
        response= fastapi.responses.RedirectResponse(url='/dashboard',status_code=status.HTTP_302_FOUND)
        return response
    else:
        return {"message": "Login failed"}
    

