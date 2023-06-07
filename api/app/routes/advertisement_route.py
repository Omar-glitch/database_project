from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.models import Advertisement
from utils.database import session
from schemas.advertisement import AdvertisementResponse, AdvertisementCreate, AdvertisementUpdate
from utils.images import save_image, remove_image

advertisement_route = APIRouter()
IMAGE_PATH = 'public/advertisements'

@advertisement_route.get('/', response_class=JSONResponse, response_model=list[AdvertisementResponse])
async def get_advertisements():
    return session.query(Advertisement).all()

@advertisement_route.get('/{id}', response_class=JSONResponse, response_model=AdvertisementResponse  )
async def get_advertisement(id : int):
    advertisement = session.get(Advertisement, id)
    if not advertisement:
        raise HTTPException(404)
    return advertisement

@advertisement_route.post('/', response_class=JSONResponse, response_model=AdvertisementResponse)
async def create_advertisement(advertisement : AdvertisementCreate = Depends()):
    filename = await save_image(advertisement.file, IMAGE_PATH)
    new_advertisement = Advertisement(
        advertisement_title = advertisement.advertisement_title,
        advertisement_description = advertisement.advertisement_description,
        advertisement_image = filename,
        owner = advertisement.owner
    )
    session.add(new_advertisement)
    session.commit()
    session.refresh(new_advertisement)
    return new_advertisement

@advertisement_route.put('/{id}', response_class=JSONResponse)
async def update_advertisement(id : int, new_advertisement: AdvertisementUpdate = Depends()):
    db_advertisement = session.get(Advertisement, id)
    if not db_advertisement:
        raise HTTPException(404)
    advertisement_data = new_advertisement.dict(exclude_unset=True, exclude_none=True)
    for key, value in advertisement_data.items():
        setattr(db_advertisement, key, value)
    session.add(db_advertisement)
    session.commit()
    session.refresh(db_advertisement)
    return db_advertisement

@advertisement_route.delete('/{id}', status_code=204, response_class=Response)
async def delete_advertisement(id : int):
    db_advertisement = session.get(Advertisement, id)
    if not db_advertisement:
        raise HTTPException(404)
    await remove_image(db_advertisement.advertisement_image, IMAGE_PATH)
    session.delete(db_advertisement)
    session.commit()
