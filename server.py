from fastapi import FastAPI

import crud
from schema import CreateAdvertisementRequest, SearchAdvertisementRequest, UpdateAdvertisementRequest, \
    CreateAdvertisementResponse, GetAdvertisementResponse, SearchAdvertisementResponse, \
    UpdateAdvertisementResponse, DeleteAdvertisementResponse
from lifespan import lifespan
from dependency import SessionDependency
import models
from sqlalchemy import select
from constants import SUCCESS_RESPONSE

app = FastAPI(
    title="advertisement API",
    description="list of advertisements",
    lifespan=lifespan
)

@app.post("/api/v1/advertisement/", tags=["advertisement"], response_model=CreateAdvertisementResponse)
async def create_advertisement(advertisement: CreateAdvertisementRequest, session: SessionDependency):
    advertisement_dict = advertisement.model_dump(exclude_unset=True)
    advertisement_orm = models.Advertisement(**advertisement_dict)
    await crud.add_item(session, advertisement_orm)
    return advertisement_orm.id_dict


@app.get("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"], response_model=GetAdvertisementResponse)
async def get_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement_orm = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    return advertisement_orm.dict

@app.get("/api/v1/advertisement/", tags=["advertisement"], response_model=SearchAdvertisementResponse)
async def search_advertisement(advertisement_data: SearchAdvertisementRequest, session: SessionDependency):
    query = (
        select(models.Advertisement).
        where(models.Advertisement.title == advertisement_data["title"],
              models.Advertisement.description == advertisement_data["description"],
              models.Advertisement.price == advertisement_data["price"],
              models.Advertisement.author == advertisement_data["author"],
              models.Advertisement.created_at == advertisement_data["created_at"]
        )
    )
    advertisements = await session.scalars(query)
    return {'results': [advertisement.dict for advertisement in advertisements]}

@app.patch("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"], response_model=UpdateAdvertisementResponse)
async def update_advertisement(advertisement_id: int, advertisement_data: UpdateAdvertisementRequest, session: SessionDependency):
    advertisement_dict = advertisement_data.model_dump(exclude_unset=True)
    advertisement_orm = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    for field, value in advertisement_dict.items():
        setattr(advertisement_orm, field, value)
    await crud.add_item(session, advertisement_orm)
    return SUCCESS_RESPONSE

@app.delete("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"], response_model=DeleteAdvertisementResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement_orm = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    await crud.delete_item(session, advertisement_orm)
    return SUCCESS_RESPONSE