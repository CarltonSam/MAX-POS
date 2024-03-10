from fastapi import FastAPI,APIRouter,Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import get_db
from routers.models import ItemDetails
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import create_engine,or_
from sqlalchemy.orm import sessionmaker

router = APIRouter()

class items(BaseModel):
    item_id : str
    item_name : str
    price : str

@router.post('/createItems')
async def create_customer(details:items,db: Session = Depends(get_db)):
    item_details = db.query(ItemDetails).filter(or_(ItemDetails.item_id == details.item_id, ItemDetails.item_name == details.item_name)).first()
    if item_details:
        return {"message" : "item with same item id or item name already exists"}
    else:
        db_item = ItemDetails(
            item_id = details.item_id,
            item_name = details.item_name,
            price = details.price
            )
    db.add(db_item)
    db.commit()
    return {"message" : "Item Details Added!"}