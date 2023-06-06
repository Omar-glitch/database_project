from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

class CategoryBase(BaseModel):
    name : str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name : Optional[str] = None


class CategoryResponse(CategoryBase):
    category_id : int

    class Config:
        orm_mode = True


class ProductImageBase(BaseModel):
    pass


class ProductImageCreate(ProductImageBase):
    product_id : str
    file : UploadFile


class ProductImageUpdate(ProductImageBase):
    product_id : Optional[int] = None
    file : Optional[UploadFile] = None


class ProductImageResponse(ProductImageBase):
    product_id : int
    name : str

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name : str
    code : str 
    description : str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name : Optional[str] = None
    code : Optional[str] = None
    description : Optional[str] = None


class ProductResponse(ProductBase):
    product_id : int

    class Config:
        orm_mode = True


class ProductCategoryBase(BaseModel):
    category_id : int
    product_id : int


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(BaseModel):
    category_id : Optional[int] = None
    product_id : Optional[int] = None


class ProductCategoryResponse(ProductCategoryBase):
    pass

    class Config:
        orm_mode = True

