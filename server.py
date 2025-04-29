from fastapi import FastAPI
from schema import CreateAdvertisementRequest, SearchAdvertisementRequest, UpdateAdvertisementRequest, \
    CreateAdvertisementResponse, GetAdvertisementResponse, SearchAdvertisementResponse, \
    UpdateAdvertisementResponse, DeleteAdvertisementResponse
from lifespan import lifespan

app = FastAPI(
    title="advertisement API",
    description="list of advertisements",
    lifespan=lifespan
)

@app.post("/api/v1/advertisement/", tags=["advertisement"], response_model=CreateAdvertisementResponse)
async def create_advertisement(advertisement: CreateAdvertisementRequest):
    pass


@app.get("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"], response_model=GetAdvertisementResponse)
async def get_advertisement(advertisement_id: int):
    pass

@app.get("/api/v1/advertisement/", tags=["advertisement"], response_model=SearchAdvertisementResponse)
async def search_advertisement(advertisement_data: SearchAdvertisementRequest):
    pass

@app.patch("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"], response_model=UpdateAdvertisementResponse)
async def update_advertisement(advertisement_id: int, advertisement_data: UpdateAdvertisementRequest):
    pass

@app.delete("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"], response_model=DeleteAdvertisementResponse)
async def delete_advertisement(advertisement_id: int):
    pass