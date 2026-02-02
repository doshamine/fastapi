from fastapi import FastAPI, HTTPException, status
import crud
from auth import hash_password, check_password
from schema import *
from lifespan import lifespan
from dependency import SessionDependency, TokenDependency
import models
from sqlalchemy import select, and_
from constants import SUCCESS_RESPONSE
from responses import responses

app = FastAPI(
    title="Advertisement API",
    description="API для размещения рекламных объявлений",
    lifespan=lifespan,
    version="0.0.1")


@app.post(
    "/api/v1/advertisement/", tags=["advertisement"],
    response_model=CreateAdvertisementResponse,
    responses={401: responses[401]})
async def create_advertisement(
        advertisement: CreateAdvertisementRequest,
        session: SessionDependency,
        token: TokenDependency):
    advertisement_dict = advertisement.model_dump(exclude_unset=True)
    advertisement_orm = models.Advertisement(**advertisement_dict,
                                             user_id=token.user_id)
    await crud.add_item(session, advertisement_orm)
    return advertisement_orm.id_dict


@app.get(
    "/api/v1/advertisement/{advertisement_id}", tags=["advertisement"],
    response_model=GetAdvertisementResponse, responses={404: responses[404]})
async def get_advertisement(
        advertisement_id: int,
        session: SessionDependency):

    advertisement_orm = await crud.get_item_by_id(session, models.Advertisement,
                                                  advertisement_id)
    return advertisement_orm.dict



@app.get(
    "/api/v1/advertisement/", tags=["advertisement"],
    response_model=SearchAdvertisementResponse)
async def search_advertisement(
        advertisement_data: SearchAdvertisementRequest,
        session: SessionDependency):
    filters = []
    data = advertisement_data.model_dump(exclude_none=True)

    query = (select(models.Advertisement))
    for field_name, value in data.items():
        field = getattr(models.Advertisement, field_name)
        if field is not None:
            filters.append(field == value)
    query = query.where(and_(*filters))

    advertisements = await session.scalars(query)
    return {'results': [advertisement.dict
                        for advertisement in advertisements.unique()]}


@app.patch(
    "/api/v1/advertisement/{advertisement_id}",
    tags=["advertisement"],
    response_model=UpdateAdvertisementResponse,
    responses=responses)
async def update_advertisement(
        advertisement_id: int, advertisement_data: UpdateAdvertisementRequest,
        session: SessionDependency, token: TokenDependency):
    advertisement_dict = advertisement_data.model_dump(exclude_unset=True)
    advertisement_orm = await crud.get_item_by_id(session, models.Advertisement,
                                                  advertisement_id)
    if token.user.role == "admin" or advertisement_orm.user_id == token.user_id:
        for field, value in advertisement_dict.items():
            setattr(advertisement_orm, field, value)
        await crud.add_item(session, advertisement_orm)
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@app.delete(
    "/api/v1/advertisement/{advertisement_id}",
    tags=["advertisement"],
    response_model=DeleteAdvertisementResponse,
    responses=responses)
async def delete_advertisement(
    advertisement_id: int, session: SessionDependency,
    token: TokenDependency):
    advertisement_orm = await crud.get_item_by_id(session, models.Advertisement,
                                                  advertisement_id)
    if token.user.role == "admin" or advertisement_orm.user_id == token.user_id:
        await crud.delete_item(session, advertisement_orm)
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@app.post(
    "/api/v1/user/", tags=["user"],
    response_model=CreateUserResponse)
async def create_user(
        user_data: CreateUserRequest,
        session: SessionDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = hash_password(user_dict["password"])
    user_orm_obj = models.User(**user_dict)
    await crud.add_item(session, user_orm_obj)
    return user_orm_obj.id_dict


@app.get(
    "/api/v1/user/{user_id}", tags=["user"],
    response_model=GetUserResponse,
    responses={404: responses[404]})
async def get_user(user_id: int, session: SessionDependency):
    user_orm = await crud.get_item_by_id(session, models.User, user_id)
    return user_orm.dict


@app.patch(
    "/api/v1/user/{user_id}", tags=["user"],
    response_model=UpdateUserResponse,
    responses=responses)
async def update_user(
        user_id: int, user_data: UpdateUserRequest,
        session: SessionDependency, token: TokenDependency):
    
    user_dict = user_data.model_dump(exclude_unset=True)
    user_orm = await crud.get_item_by_id(session, models.User, user_id)

    if token.user.role == "admin" or user_orm.id == token.user_id:
        for field, value in user_dict.items():
            setattr(user_orm, field, value)
        await crud.add_item(session, user_orm)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Insufficient privileges")


@app.delete(
    "/api/v1/user/{user_id}", tags=["user"],
    response_model=DeleteUserResponse,
    responses=responses)
async def delete_user(
        user_id: int, session: SessionDependency,
        token: TokenDependency):
    
    user_orm = await crud.get_item_by_id(session, models.User, user_id)
    if token.user.role == "admin" or user_orm.id == token.user_id:
        await crud.delete_item(session, user_orm)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Insufficient privileges")


@app.post("/api/v1/login/", tags=["login"],
          response_model=LoginResponse, responses={401: responses[401]})
async def login(login_data: LoginRequest, session: SessionDependency):
    
    query = select(models.User).where(models.User.name == login_data.name)
    user = await session.scalar(query)
    if user is None or not check_password(login_data.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = models.Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict
