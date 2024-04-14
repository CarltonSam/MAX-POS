import fastapi
from fastapi import FastAPI,APIRouter,Depends,status,Request,Form
from sqlalchemy.orm import Session
from . import get_db
from routers.models import ItemDetails
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

@router.get('/items',response_class=HTMLResponse,include_in_schema=False)
def form(request:Request,db: Session = Depends(get_db)):
    all_items = db.query(ItemDetails).all()
    print(all_items)
    return templates.TemplateResponse("/items.html",{"request":request,"items":all_items})

@router.post('/createItems')
async def create_customer(item_id: str = Form(...), item_name: str = Form(...), price: str = Form(...), db: Session = Depends(get_db)):
    item_details = db.query(ItemDetails).filter(or_(ItemDetails.item_id == item_id, ItemDetails.item_name == item_name)).first()
    if item_details:
        return {"message": "item with same item id or item name already exists"}
    else:
        db_item = ItemDetails(
            item_id=item_id,
            item_name=item_name,
            price=price
        )
        db.add(db_item)
        db.commit()
        response = RedirectResponse(url='/items', status_code=status.HTTP_302_FOUND)
        return response