from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from routers.models import UserDetails
from routers import login, customerdetails,dashboarddetails, itemdetails,orderdetails
from fastapi import FastAPI, APIRouter, Depends, Request
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from routers.models import ItemDetails
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(login.router)
app.include_router(customerdetails.router)
app.include_router(itemdetails.router)
app.include_router(orderdetails.router)
app.include_router(dashboarddetails.router)

