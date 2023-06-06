from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

class PharmacyImageBase(BaseModel):
    pass


class PharmacyImageCreate(PharmacyImageBase):
    pharmacy_id : str
    file : UploadFile


class PharmacyImageUpdate(PharmacyImageBase):
    pharmacy_id : Optional[int] = None
    file : Optional[UploadFile] = None


class PharmacyImageResponse(PharmacyImageBase):
    pharmacy_id : int
    name : str

    class Config:
        orm_mode = True


class PharmacyBase(BaseModel):
    name : str
    address : str
    lat : float
    lng : float
    contact : str
    owner : int


class PharmacyCreate(PharmacyBase):
    pass


class PharmacyUpdate(BaseModel):
    name : Optional[str] = None
    address : Optional[str] = None
    lat : Optional[float] = None
    lng : Optional[float] = None
    contact : Optional[str] = None
    owner : Optional[int] = None


class PharmacyResponse(PharmacyBase):
    pharmacy_id : int
    images : list[PharmacyImageResponse]

    class Config:
        orm_mode = True
