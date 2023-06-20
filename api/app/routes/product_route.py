from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.database import session
from utils.models import Product, ProductImage, ProductCategory, Category, Inventory
from schemas.product import ProductImageResponse, ProductImageCreate, ProductImageUpdate, ProductCreate, ProductUpdate, ProductResponse, CategoryCreate, CategoryResponse, CategoryUpdate, ProductCategoryCreate, ProductCategoryUpdate, ProductCategoryResponse
from utils.images import save_image, remove_image

product_route = APIRouter()
IMAGE_PATH = 'public/products'

async def check_product_and_category(p_id, c_id, collision = True):
    if collision and session.get(ProductCategory, (p_id, c_id)):
        raise HTTPException(400, 'this combination of keys already exists')

async def check_product_category(product_id, category_id):
    category = session.get(ProductCategory, (product_id, category_id))
    if not category:
        raise HTTPException(404, 'product_category does not exist')
    return category

async def check_product(id):
    if id != None:
        product = session.get(Product, id)
        if not product:
            raise HTTPException(404, 'product does not exist')
        return product

async def check_category(id):
    if id != None:
        category = session.get(Category, id)
        if not category:
            raise HTTPException(404, 'category does not exist')
        return category

async def check_img(id):
    product_image = session.get(ProductImage, id)
    if not product_image:
        raise HTTPException(404, 'image does not exist')
    return product_image

@product_route.get('/product_category', response_class=JSONResponse, response_model=list[ProductCategoryResponse])
async def get_product_categories(skip : int = 0, limit : int = 100):
    return session.query(ProductCategory).offset(skip).limit(limit).all()

@product_route.get('/product_category/{product_id}', response_class=JSONResponse, response_model=ProductCategoryResponse  )
async def get_product_category(product_id : int, category_id):
   return await check_product_category(product_id, category_id)

@product_route.post('/product_category', response_class=JSONResponse, response_model=ProductCategoryResponse)
async def create_product_category(product_category : ProductCategoryCreate = Depends()):
    await check_product_and_category(product_category.product_id, product_category.category_id)
    await check_category(product_category.category_id)
    await check_product(product_category.product_id)
    new_product_category = ProductCategory(**product_category.dict())
    session.add(new_product_category)
    session.commit()
    session.refresh(new_product_category)
    return new_product_category

@product_route.put('/product_category/{current_product_id}', response_class=JSONResponse)
async def update_product_category(current_product_id : int, current_category_id : int, new_product_category: ProductCategoryUpdate = Depends()):
    db_product_category = await check_product_category(current_product_id, current_category_id)
    await check_product_and_category(new_product_category.product_id, new_product_category.category_id)
    await check_category(new_product_category.category_id)
    await check_product(new_product_category.product_id)
    product_category_data = new_product_category.dict(exclude_unset=True, exclude_none=True)
    for key, value in product_category_data.items():
        setattr(db_product_category, key, value)
    session.add(db_product_category)
    session.commit()
    session.refresh(db_product_category)
    return db_product_category

@product_route.delete('/product_category/{product_id}', status_code=204, response_class=Response)
async def delete_product_category(product_id : int, category_id : int):
    db_product_category = await check_product_category(product_id, category_id)
    session.delete(db_product_category)
    session.commit()

@product_route.get('/category', response_class=JSONResponse, response_model=list[CategoryResponse])
async def get_categories(skip : int = 0, limit : int = 100):
    return session.query(Category).offset(skip).limit(limit).all()

@product_route.get('/category/{id}', response_class=JSONResponse, response_model=CategoryResponse  )
async def get_category(id : int):
    return await check_category(id)

@product_route.post('/category', response_class=JSONResponse, response_model=CategoryResponse)
async def create_category(category : CategoryCreate = Depends()):
    new_category = Category(**category.dict())
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

@product_route.put('/category/{id}', response_class=JSONResponse)
async def update_category(id : int, new_category: CategoryUpdate = Depends()):
    db_category = await check_category(id)
    category_data = new_category.dict(exclude_unset=True, exclude_none=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@product_route.delete('/category/{id}', status_code=204, response_class=Response)
async def delete_category(id : int):
    if session.query(ProductCategory).filter(ProductCategory.category_id == id).first():
        raise HTTPException(400, 'cannot delete because it has relationship in product_category table')
    db_category = await check_category(id)
    session.delete(db_category)
    session.commit()

@product_route.get('/image', response_class=JSONResponse, response_model=list[ProductImageResponse])
async def get_product_images(skip : int = 0, limit : int = 100):
    return session.query(ProductImage).offset(skip).limit(limit).all()

@product_route.get('/image/{id}', response_class=JSONResponse, response_model=ProductImageResponse)
async def get_product_image(id : str):
    return await check_img(id)

@product_route.post('/image', response_class=JSONResponse, response_model=ProductImageResponse)
async def create_product_image(product_image : ProductImageCreate = Depends()):
    await check_product(product_image.product_id)
    filename = await save_image(product_image.name, dest=IMAGE_PATH)
    new_image = ProductImage(name = filename, product_id = product_image.product_id)
    session.add(new_image)
    session.commit()
    session.refresh(new_image)
    return new_image

@product_route.put('/image/{id}', response_class=JSONResponse)
async def update_product_image(id : str, new_image: ProductImageUpdate = Depends()):
    db_image = await check_img(id)
    if new_image.name != None:
        await remove_image(db_image.name, IMAGE_PATH)
        new_image.name = await save_image(new_image.name, IMAGE_PATH)
    image_data = new_image.dict(exclude_unset=True, exclude_none=True)
    for key, value in image_data.items():
        setattr(db_image, key, value)
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image

@product_route.delete('/image/{id}', status_code=204, response_class=Response)
async def delete_product_image(id : str):
    db_image = await check_img(id)
    await remove_image(id, IMAGE_PATH)
    session.delete(db_image)
    session.commit()

@product_route.get('/', response_class=JSONResponse, response_model=list[ProductResponse])
async def get_products(skip : int = 0, limit : int = 100):
    return session.query(Product).offset(skip).limit(limit).all()

@product_route.get('/{id}', response_class=JSONResponse, response_model=ProductResponse)
async def get_product(id : int):
    return await check_product(id)

@product_route.post('/', response_class=JSONResponse, response_model=ProductResponse)
async def create_product(product : ProductCreate = Depends()):
    new_product = Product(**product.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@product_route.put('/{id}', response_class=JSONResponse)
async def update_product(id : int, new_product: ProductUpdate = Depends()):
    db_product = await check_product(id)
    product_data = new_product.dict(exclude_unset=True, exclude_none=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@product_route.delete('/{id}', status_code=204, response_class=Response)
async def delete_product(id : int):
    db_product = await check_product(id)
    if session.query(Inventory).filter(Inventory.product_id == id).first():
        raise HTTPException(400, 'cannot delete because this product is in inventories')
    if session.query(ProductCategory).filter(ProductCategory.product_id == id).first():
        raise HTTPException(400, 'cannot delete because this product is in product_category')
    imgs = session.query(ProductImage).filter(ProductImage.product_id == id).all()
    for img in imgs:
        await remove_image(img.name, IMAGE_PATH)
        session.delete(img)
        session.commit()
    session.delete(db_product)
    session.commit()
