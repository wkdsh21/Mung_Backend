from datetime import datetime
from typing import Literal, Annotated

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