from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

class AdvertisementBase(BaseModel):
    advertisement_title : str
    advertisement_description : str
    owner : int


class AdvertisementCreate(AdvertisementBase):
    file : UploadFile


class AdvertisementUpdate(BaseModel):
    advertisement_title : Optional[str] = None
    advertisement_description : Optional[str] = None
    advertisement_image : Optional[UploadFile] = None
    owner : Optional[int] = None
    

class AdvertisementResponse(AdvertisementBase):
    advertisement_id : int
    advertisement_image : str

    class Config:
        orm_mode = True
