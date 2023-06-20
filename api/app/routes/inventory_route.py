from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.database import session
from utils.models import Inventory, Product, Pharmacy
from schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse

inventory_route = APIRouter()

async def check_product_and_pharmacy(product_id, pharmacy_id, collision = True):
    if product_id != None:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(404, 'product does not exist')
    if pharmacy_id != None:
        db_pharmacy = session.get(Pharmacy, pharmacy_id)
        if not db_pharmacy:
            raise HTTPException(404, 'pharmacy does not exist')
    if collision and session.get(Inventory, (product_id, pharmacy_id)):
        raise HTTPException(400, 'this combination of keys already exists')
        
async def check_inventory(product_id, pharmacy_id):
    db_inventory = session.get(Inventory, (product_id, pharmacy_id))
    if not db_inventory:
        raise HTTPException(404, 'inventory does not exist')
    return db_inventory

@inventory_route.get('/', response_class=JSONResponse, response_model=list[InventoryResponse])
async def get_inventories(skip : int = 0, limit : int = 100):
    return session.query(Inventory).offset(skip).limit(limit).all()

@inventory_route.get('/{product_id}', response_class=JSONResponse, response_model=InventoryResponse  )
async def get_inventory(product_id : int, pharmacy_id : int):
    return await check_inventory(product_id, pharmacy_id)

@inventory_route.post('/', response_class=JSONResponse, response_model=InventoryResponse)
async def create_inventory(inventory : InventoryCreate = Depends()):
    await check_product_and_pharmacy(inventory.product_id, inventory.pharmacy_id)
    new_inventory = Inventory(**inventory.dict())
    session.add(new_inventory)
    session.commit()
    session.refresh(new_inventory)
    return new_inventory

@inventory_route.put('/{current_product_id}', response_class=JSONResponse)
async def update_inventory(current_product_id : int, current_pharmacy_id : int, new_inventory: InventoryUpdate = Depends()):
    await check_product_and_pharmacy(new_inventory.product_id, new_inventory.pharmacy_id)
    db_inventory = await check_inventory(current_product_id, current_pharmacy_id)
    inventory_data = new_inventory.dict(exclude_unset=True, exclude_none=True)
    for key, value in inventory_data.items():
        setattr(db_inventory, key, value)
    session.add(db_inventory)
    session.commit()
    session.refresh(db_inventory)
    return db_inventory

@inventory_route.delete('/{product_id}', status_code=204, response_class=Response)
async def delete_inventory(product_id : int, pharmacy_id : int):
    db_inventory = await check_inventory(product_id, pharmacy_id)
    session.delete(db_inventory)
    session.commit()
