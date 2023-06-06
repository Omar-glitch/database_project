from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.database import session
from utils.models import Pharmacy, PharmacyImage
from schemas.pharmacy import PharmacyCreate, PharmacyResponse, PharmacyUpdate, PharmacyImageCreate, PharmacyImageResponse, PharmacyImageUpdate
from utils.images import save_image, remove_image

pharmacy_route = APIRouter()

@pharmacy_route.get('/image', response_class=JSONResponse, response_model=list[PharmacyImageResponse])
async def get_pharmacie_images():
    return session.query(PharmacyImage).all()

@pharmacy_route.get('/image/{id}', response_class=JSONResponse, response_model=PharmacyImageResponse)
async def get_pharmacy_image(id : int):
    pharmacy_image = session.get(PharmacyImage, id)
    if not pharmacy_image:
        raise HTTPException(404)
    return pharmacy_image

@pharmacy_route.post('/image', response_class=JSONResponse, response_model=PharmacyImageResponse)
async def create_pharmacy_image(pharmacy_image : PharmacyImageCreate = Depends()):
    filename = await save_image(pharmacy_image.file, dest='public/pharmacies')
    new_image = PharmacyImage(name = filename, pharmacy_id = pharmacy_image.pharmacy_id)
    session.add(new_image)
    session.commit()
    session.refresh(new_image)
    return new_image

@pharmacy_route.put('/image/{id}', response_class=JSONResponse)
async def update_pharmacy_image(id : str, new_image: PharmacyImageUpdate = Depends()):
    db_image = session.get(PharmacyImage, id)
    if not db_image:
        raise HTTPException(404)
    image_data = new_image.dict(exclude_unset=True, exclude_none=True)
    for key, value in image_data.items():
        setattr(db_image, key, value)
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image

@pharmacy_route.delete('/image/{id}', status_code=204, response_class=Response)
async def delete_pharmacy_image(id : str):
    db_image = session.get(PharmacyImage, id)
    if not db_image:
        raise HTTPException(404)
    await remove_image(id, 'public/pharmacies')
    session.delete(db_image)
    session.commit()

@pharmacy_route.get('/', response_class=JSONResponse, response_model=list[PharmacyResponse])
async def get_pharmacies():
    return session.query(Pharmacy).all()

@pharmacy_route.get('/{id}', response_class=JSONResponse, response_model=PharmacyResponse)
async def get_pharmacy(id : int):
    pharmacy = session.get(Pharmacy, id)
    if not pharmacy:
        raise HTTPException(404)
    return pharmacy

@pharmacy_route.post('/', response_class=JSONResponse, response_model=PharmacyResponse)
async def create_pharmacy(pharmacy : PharmacyCreate = Depends()):
    new_pharmacy = Pharmacy(**pharmacy.dict())
    session.add(new_pharmacy)
    session.commit()
    session.refresh(new_pharmacy)
    return new_pharmacy

@pharmacy_route.put('/{id}', response_class=JSONResponse)
async def update_pharmacy(id : int, new_pharmacy: PharmacyUpdate = Depends()):
    db_pharmacy = session.get(Pharmacy, id)
    if not db_pharmacy:
        raise HTTPException(404)
    pharmacy_data = new_pharmacy.dict(exclude_unset=True, exclude_none=True)
    for key, value in pharmacy_data.items():
        setattr(db_pharmacy, key, value)
    session.add(db_pharmacy)
    session.commit()
    session.refresh(db_pharmacy)
    return db_pharmacy

@pharmacy_route.delete('/{id}', status_code=204, response_class=Response)
async def delete_pharmacy(id : int):
    db_pharmacy = session.get(Pharmacy, id)
    if not db_pharmacy:
        raise HTTPException(404)
    session.delete(db_pharmacy)
    session.commit()
