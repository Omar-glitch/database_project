from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.database import session
from utils.models import Inventory
from schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse

inventory_route = APIRouter()

@inventory_route.get('/', response_class=JSONResponse, response_model=list[InventoryResponse])
async def get_inventories():
    return session.query(Inventory).all()

@inventory_route.get('/{product_id}', response_class=JSONResponse, response_model=InventoryResponse  )
async def get_inventory(product_id : int, category_id):
    inventory = session.get(Inventory, (product_id, category_id))
    if not inventory:
        raise HTTPException(404)
    return inventory

@inventory_route.post('/', response_class=JSONResponse, response_model=InventoryResponse)
async def create_inventory(inventory : InventoryCreate = Depends()):
    new_inventory = Inventory(**inventory.dict())
    session.add(new_inventory)
    session.commit()
    session.refresh(new_inventory)
    return new_inventory

@inventory_route.put('/{product_id}', response_class=JSONResponse)
async def update_inventory(product_id : int, category_id : int, new_inventory: InventoryUpdate = Depends()):
    db_inventory = session.get(Inventory, (product_id, category_id))
    if not db_inventory:
        raise HTTPException(404)
    inventory_data = new_inventory.dict(exclude_unset=True, exclude_none=True)
    for key, value in inventory_data.items():
        setattr(db_inventory, key, value)
    session.add(db_inventory)
    session.commit()
    session.refresh(db_inventory)
    return db_inventory

@inventory_route.delete('/{product_id}', status_code=204, response_class=Response)
async def delete_inventory(product_id : int, category_id : int):
    db_inventory = session.get(Inventory, (product_id, category_id))
    if not db_inventory:
        raise HTTPException(404)
    session.delete(db_inventory)
    session.commit()