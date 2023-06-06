from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from utils.database import session
from utils.models import User, UserType
from schemas.user import UserCreate, UserResponse, UserTypeResponse, UserTypeCreate, UserTypeUpdate, UserUpdate

user_route = APIRouter()

@user_route.get('/type', response_class=JSONResponse, response_model=list[UserTypeResponse])
async def get_user_types():
    return session.query(UserType).all()

@user_route.get('/type/{id}', response_class=JSONResponse, response_model=UserTypeResponse  )
async def get_user_type(id : int):
    type = session.get(UserType, id)
    if not type:
        raise HTTPException(404)
    return type

@user_route.post('/type', response_class=JSONResponse, response_model=UserTypeResponse)
async def create_user_type(type : UserTypeCreate = Depends()):
    new_type = UserType(**type.dict())
    session.add(new_type)
    session.commit()
    session.refresh(new_type)
    return new_type

@user_route.put('/type/{id}', response_class=JSONResponse)
async def update_user_type(id : int, new_type: UserTypeUpdate = Depends()):
    db_type = session.get(UserType, id)
    if not db_type:
        raise HTTPException(404)
    type_data = new_type.dict(exclude_unset=True, exclude_none=True)
    for key, value in type_data.items():
        setattr(db_type, key, value)
    session.add(db_type)
    session.commit()
    session.refresh(db_type)
    return db_type

@user_route.delete('/type/{id}', status_code=204, response_class=Response)
async def delete_user_type(id : int):
    db_user_type = session.get(UserType, id)
    if not db_user_type:
        raise HTTPException(404)
    session.delete(db_user_type)
    session.commit()

@user_route.get('/', response_class=JSONResponse, response_model=list[UserResponse])
async def get_users(skip: int = 0, limit : int = 10): 
    return session.query(User).offset(skip).limit(limit).all()

@user_route.get('/{id}', response_class=JSONResponse, response_model=UserResponse)
async def get_user(id : int): 
    user = session.get(User, id)
    if not user:
        raise HTTPException(404)
    return user

@user_route.post('/', response_class=JSONResponse, response_model=UserResponse)
async def create_user(user : UserCreate = Depends()):
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@user_route.put('/{id}', response_class=JSONResponse)
async def update_user(id : int, new_user : UserUpdate = Depends()):
    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(404)
    user_data = new_user.dict(exclude_unset=True, exclude_none=True)
    print(user_data)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@user_route.delete('/{id}', response_class=Response, status_code=204)
async def delete_user(id : int):
    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(404)
    session.delete(db_user)
    session.commit()
