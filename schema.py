import uuid

from pydantic import BaseModel
import datetime
from typing import Literal


class IdResponse(BaseModel):
    id: int


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str | None = None
    price: float
    author: str
    created_at: datetime.datetime | None = None


class SearchAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None
    created_at: datetime.datetime | None = None


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None
    created_at: datetime.datetime | None = None


class CreateAdvertisementResponse(IdResponse):
    pass


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


class BaseUserRequest(BaseModel):
    name: str
    password: str
    role: str | None = None


class LoginRequest(BaseUserRequest):
    pass


class LoginResponse(BaseModel):
    token: uuid.UUID


class CreateUserRequest(BaseUserRequest):
    pass


class UpdateUserRequest(BaseModel):
    name: str | None = None
    password: str | None = None
    role: str | None = None


class CreateUserResponse(IdResponse):
    pass


class GetUserResponse(BaseModel):
    id: int
    name: str
    role: str


class UpdateUserResponse(SuccessResponse):
    pass


class DeleteUserResponse(SuccessResponse):
    pass
