from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.database import session
from utils.models import Pharmacy, PharmacyImage, User, Inventory
from schemas.pharmacy import PharmacyCreate, PharmacyResponse, PharmacyUpdate, PharmacyImageCreate, PharmacyImageResponse, PharmacyImageUpdate
from utils.images import save_image, remove_image

pharmacy_route = APIRouter()
IMAGE_PATH = 'public/pharmacies'

async def check_pharmacy(id):
    if id != None:
        pharmacy = session.get(Pharmacy, id)
        if not pharmacy:
            raise HTTPException(404, 'pharmacy does not exist')
        return pharmacy

async def check_pharmacy_img(id):
    image = session.get(PharmacyImage, id)
    if not image:
        raise HTTPException(404, 'pharmacy image does not exist')
    return image

async def check_owner(id):
    if id != None:
        owner = session.get(User, id)
        if not owner:
            raise HTTPException(404, 'owner does not exist')

@pharmacy_route.get('/image', response_class=JSONResponse, response_model=list[PharmacyImageResponse])
async def get_pharmacie_images(skip : int = 0, limit : int = 100):
    return session.query(PharmacyImage).offset(skip).limit(limit).all()

@pharmacy_route.get('/image/{id}', response_class=JSONResponse, response_model=PharmacyImageResponse)
async def get_pharmacy_image(id : str):
    return await check_pharmacy_img(id)

@pharmacy_route.post('/image', response_class=JSONResponse, response_model=PharmacyImageResponse)
async def create_pharmacy_image(pharmacy_image : PharmacyImageCreate = Depends()):
    await check_pharmacy(pharmacy_image.pharmacy_id)
    filename = await save_image(pharmacy_image.name, dest=IMAGE_PATH)
    new_image = PharmacyImage(name = filename, pharmacy_id = pharmacy_image.pharmacy_id)
    session.add(new_image)
    session.commit()
    session.refresh(new_image)
    return new_image

@pharmacy_route.put('/image/{id}', response_class=JSONResponse)
async def update_pharmacy_image(id : str, new_image: PharmacyImageUpdate = Depends()):
    await check_pharmacy(new_image.pharmacy_id)
    db_image = await check_pharmacy_img(id)
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

@pharmacy_route.delete('/image/{id}', status_code=204, response_class=Response)
async def delete_pharmacy_image(id : str):
    db_image = await check_pharmacy_img(id)
    await remove_image(id, IMAGE_PATH)
    session.delete(db_image)
    session.commit()

@pharmacy_route.get('/', response_class=JSONResponse, response_model=list[PharmacyResponse])
async def get_pharmacies(skip : int = 0, limit : int = 100):
    return session.query(Pharmacy).offset(skip).limit(limit).all()

@pharmacy_route.get('/{id}', response_class=JSONResponse, response_model=PharmacyResponse)
async def get_pharmacy(id : int):
    return await check_pharmacy(id)

@pharmacy_route.post('/', response_class=JSONResponse, response_model=PharmacyResponse)
async def create_pharmacy(pharmacy : PharmacyCreate = Depends()):
    await check_owner(pharmacy.owner)
    new_pharmacy = Pharmacy(**pharmacy.dict())
    session.add(new_pharmacy)
    session.commit()
    session.refresh(new_pharmacy)
    return new_pharmacy

@pharmacy_route.put('/{id}', response_class=JSONResponse)
async def update_pharmacy(id : int, new_pharmacy: PharmacyUpdate = Depends()):
    await check_owner(new_pharmacy.owner)
    db_pharmacy = await check_pharmacy(id)
    pharmacy_data = new_pharmacy.dict(exclude_unset=True, exclude_none=True)
    for key, value in pharmacy_data.items():
        setattr(db_pharmacy, key, value)
    session.add(db_pharmacy)
    session.commit()
    session.refresh(db_pharmacy)
    return db_pharmacy

@pharmacy_route.delete('/{id}', status_code=204, response_class=Response)
async def delete_pharmacy(id : int):
    db_pharmacy = await check_pharmacy(id)
    inventory = session.query(Inventory).filter(Inventory.pharmacy_id == id).first()
    if inventory:
        raise HTTPException(400, 'cannot delete because this pharmacy has inventories')
    imgs = session.query(PharmacyImage).filter(PharmacyImage.pharmacy_id == id).all()
    for img in imgs:
        await remove_image(img.name, IMAGE_PATH)
        session.delete(img)
        session.commit()
    session.delete(db_pharmacy)
    session.commit()
