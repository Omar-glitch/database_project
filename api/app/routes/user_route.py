from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.database import session
from utils.models import User, UserType, Advertisement, Pharmacy
from schemas.user import UserCreate, UserResponse, UserTypeResponse, UserTypeCreate, UserTypeUpdate, UserUpdate

user_route = APIRouter()

async def check_type(id):
    if id != None:
        type = session.get(UserType, id)
        if not type:
            raise HTTPException(404, 'could not find type')
        return type

async def check_user(id):
    user = session.get(User, id)
    if not user:
        raise HTTPException(404, 'user not found')
    return user

@user_route.get('/type', response_class=JSONResponse, response_model=list[UserTypeResponse])
async def get_user_types(skip : int = 0, limit : int = 100):
    return session.query(UserType).offset(skip).limit(limit).all()

@user_route.get('/type/{id}', response_class=JSONResponse, response_model=UserTypeResponse  )
async def get_user_type(id : int):
    return await check_type(id)

@user_route.post('/type', response_class=JSONResponse, response_model=UserTypeResponse)
async def create_user_type(type : UserTypeCreate = Depends()):
    new_type = UserType(**type.dict())
    session.add(new_type)
    session.commit()
    session.refresh(new_type)
    return new_type

@user_route.put('/type/{id}', response_class=JSONResponse)
async def update_user_type(id : int, new_type: UserTypeUpdate = Depends()):
    db_type = await check_type(id)
    type_data = new_type.dict(exclude_unset=True, exclude_none=True)
    for key, value in type_data.items():
        setattr(db_type, key, value)
    session.add(db_type)
    session.commit()
    session.refresh(db_type)
    return db_type

@user_route.delete('/type/{id}', status_code=204, response_class=Response)
async def delete_user_type(id : int):
    db_user_type = check_type(id)
    if session.query(User).filter(User.type == id).first():
        raise HTTPException(400, 'cannot remove because it still has relationship with users')
    session.delete(db_user_type)
    session.commit()

@user_route.get('/', response_class=JSONResponse, response_model=list[UserResponse])
async def get_users(skip: int = 0, limit : int = 100): 
    return session.query(User).offset(skip).limit(limit).all()

@user_route.get('/{id}', response_class=JSONResponse, response_model=UserResponse)
async def get_user(id : int): 
    return await check_user(id)

@user_route.post('/', response_class=JSONResponse, response_model=UserResponse)
async def create_user(user : UserCreate = Depends()):
    await check_type(user.type)
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@user_route.put('/{id}', response_class=JSONResponse)
async def update_user(id : int, new_user : UserUpdate = Depends()):
    db_user = await check_user(id)
    await check_type(new_user.type)
    user_data = new_user.dict(exclude_unset=True, exclude_none=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@user_route.delete('/{id}', response_class=Response, status_code=204)
async def delete_user(id : int):
    db_user = await check_user(id)
    if session.query(Advertisement).filter(Advertisement.owner == id).first():
        raise HTTPException(400, 'cannot delete user because it has advertisements')
    if session.query(Pharmacy).filter(Pharmacy.owner == id).first():
        raise HTTPException(400, 'cannot delete user because it has pharmacies')
    session.delete(db_user)
    session.commit()
