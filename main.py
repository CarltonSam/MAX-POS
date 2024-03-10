from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

from routers import login,customerdetails,itemdetails

app=FastAPI()

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

@app.get('/')
def root():
    return {'root': '/'}