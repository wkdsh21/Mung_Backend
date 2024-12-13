from datetime import datetime
from typing import Annotated, Literal

from annotated_types import Gt
from ninja import Schema


class PetCreateRequest(Schema):
    name: str
    profile_img: str
    type: str
    species: str
    is_neutering: bool
    birth_date: datetime
    weight: Annotated[float, Gt(0)]
    need_diet: bool

    class Config:
        orm_mode = True


class PetGetListResponse(Schema):
    id: int
    name: str
    profile_img: str
    type: str
    species: str
    is_neutering: bool
    birth_date: datetime
    need_diet: bool
    weight: Annotated[float, Gt(0)]

    class Config:
        orm_mode = True


class PetUpdateRequest(Schema):
    type: str
    is_neutering: bool
    birth_date: datetime
    need_diet: bool
    weight: Annotated[float, Gt(0)]

    class Config:
        orm_mode = True


class PetGetCardResponse(Schema):
    name: str
    profile_img: str

    class Config:
        orm_mode = True


class PetGetGraphResponse(Schema):
    last_modified_at: datetime
    weight: float

    class Config:
        orm_mode = True


class PetStatusMessage(Schema):
    message: str
    status: Literal["success", "error"]


class PetPatchNameRequest(Schema):
    name: str
