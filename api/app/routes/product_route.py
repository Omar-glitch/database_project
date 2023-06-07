from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.database import session
from utils.models import Product, ProductImage, ProductCategory, Category
from schemas.product import ProductImageResponse, ProductImageCreate, ProductImageUpdate, ProductCreate, ProductUpdate, ProductResponse, CategoryCreate, CategoryResponse, CategoryUpdate, ProductCategoryCreate, ProductCategoryUpdate, ProductCategoryResponse
from utils.images import save_image, remove_image

product_route = APIRouter()
IMAGE_PATH = 'public/products'

@product_route.get('/product_category', response_class=JSONResponse, response_model=list[ProductCategoryResponse])
async def get_product_categories():
    return session.query(ProductCategory).all()

@product_route.get('/product_category/{product_id}', response_class=JSONResponse, response_model=ProductCategoryResponse  )
async def get_product_category(product_id : int, category_id):
    product_category = session.get(ProductCategory, (product_id, category_id))
    if not product_category:
        raise HTTPException(404)
    return product_category

@product_route.post('/product_category', response_class=JSONResponse, response_model=ProductCategoryResponse)
async def create_product_category(product_category : ProductCategoryCreate = Depends()):
    new_product_category = ProductCategory(**product_category.dict())
    session.add(new_product_category)
    session.commit()
    session.refresh(new_product_category)
    return new_product_category

@product_route.put('/product_category/{product_id}', response_class=JSONResponse)
async def update_product_category(product_id : int, category_id : int, new_product_category: ProductCategoryUpdate = Depends()):
    db_product_category = session.get(ProductCategory, (product_id, category_id))
    if not db_product_category:
        raise HTTPException(404)
    product_category_data = new_product_category.dict(exclude_unset=True, exclude_none=True)
    for key, value in product_category_data.items():
        setattr(db_product_category, key, value)
    session.add(db_product_category)
    session.commit()
    session.refresh(db_product_category)
    return db_product_category

@product_route.delete('/product_category/{product_id}', status_code=204, response_class=Response)
async def delete_product_category(product_id : int, category_id : int):
    db_product_category = session.get(ProductCategory, (product_id, category_id))
    if not db_product_category:
        raise HTTPException(404)
    session.delete(db_product_category)
    session.commit()

@product_route.get('/category', response_class=JSONResponse, response_model=list[CategoryResponse])
async def get_categories():
    return session.query(Category).all()

@product_route.get('/category/{id}', response_class=JSONResponse, response_model=CategoryResponse  )
async def get_category(id : int):
    category = session.get(Category, id)
    if not category:
        raise HTTPException(404)
    return category

@product_route.post('/category', response_class=JSONResponse, response_model=CategoryResponse)
async def create_category(category : CategoryCreate = Depends()):
    new_category = Category(**category.dict())
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

@product_route.put('/category/{id}', response_class=JSONResponse)
async def update_category(id : int, new_category: CategoryUpdate = Depends()):
    db_category = session.get(Category, id)
    if not db_category:
        raise HTTPException(404)
    category_data = new_category.dict(exclude_unset=True, exclude_none=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@product_route.delete('/category/{id}', status_code=204, response_class=Response)
async def delete_category(id : int):
    db_category = session.get(Category, id)
    if not db_category:
        raise HTTPException(404)
    session.delete(db_category)
    session.commit()

@product_route.get('/image', response_class=JSONResponse, response_model=list[ProductImageResponse])
async def get_product_images():
    return session.query(ProductImage).all()

@product_route.get('/image/{id}', response_class=JSONResponse, response_model=ProductImageResponse)
async def get_product_image(id : str):
    product_image = session.get(ProductImage, id)
    if not product_image:
        raise HTTPException(404)
    return product_image

@product_route.post('/image', response_class=JSONResponse, response_model=ProductImageResponse)
async def create_product_image(product_image : ProductImageCreate = Depends()):
    filename = await save_image(product_image.file, dest=IMAGE_PATH)
    new_image = ProductImage(name = filename, product_id = product_image.product_id)
    session.add(new_image)
    session.commit()
    session.refresh(new_image)
    return new_image

@product_route.put('/image/{id}', response_class=JSONResponse)
async def update_product_image(id : str, new_image: ProductImageUpdate = Depends()):
    db_image = session.get(ProductImage, id)
    if not db_image:
        raise HTTPException(404)
    image_data = new_image.dict(exclude_unset=True, exclude_none=True)
    for key, value in image_data.items():
        setattr(db_image, key, value)
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image

@product_route.delete('/image/{id}', status_code=204, response_class=Response)
async def delete_product_image(id : str):
    db_image = session.get(ProductImage, id)
    if not db_image:
        raise HTTPException(404)
    await remove_image(id, IMAGE_PATH)
    session.delete(db_image)
    session.commit()

@product_route.get('/', response_class=JSONResponse, response_model=list[ProductResponse])
async def get_products():
    return session.query(Product).all()

@product_route.get('/{id}', response_class=JSONResponse, response_model=ProductResponse)
async def get_product(id : int):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(404)
    return product

@product_route.post('/', response_class=JSONResponse, response_model=ProductResponse)
async def create_product(product : ProductCreate = Depends()):
    new_product = Product(**product.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@product_route.put('/{id}', response_class=JSONResponse)
async def update_product(id : int, new_product: ProductUpdate = Depends()):
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(404)
    product_data = new_product.dict(exclude_unset=True, exclude_none=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@product_route.delete('/{id}', status_code=204, response_class=Response)
async def delete_product(id : int):
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(404)
    session.delete(db_product)
    session.commit()
