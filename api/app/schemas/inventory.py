from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

class InventoryBase(BaseModel):
    product_id : int
    pharmacy_id : int
    stock : int
    price : float

class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    product_id : Optional[int] = None
    pharmacy_id : Optional[int] = None


class InventoryResponse(InventoryBase):
    pass

    class Config:
        orm_mode = True

