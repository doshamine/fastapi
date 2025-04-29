from pydantic import BaseModel
import datetime
from typing import Literal

class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str | None = None
    price: float
    author: str
    created_at: datetime.datetime


class SearchAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: float
    author: str
    created_at: datetime.datetime


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None
    created_at: datetime.datetime | None = None


class CreateAdvertisementResponse(BaseModel):
    id: int


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: datetime.datetime


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]


class SuccessResponse(BaseModel):
    status: Literal["success"]


class UpdateAdvertisementResponse(SuccessResponse):
    pass


class DeleteAdvertisementResponse(SuccessResponse):
    pass