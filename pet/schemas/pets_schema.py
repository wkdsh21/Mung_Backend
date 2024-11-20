from datetime import datetime

from ninja import Schema


class PetCreateRequest(Schema):
    animal_name: str
    animal_img: str
    animal_type: str
    animal_species: str
    is_neutering: bool
    animal_born_in: datetime
    animal_weight: float
    need_diet: bool

    class Config:
        orm_mode = True


class PetGetListResponse(Schema):
    animal_name: str
    animal_img: str
    animal_type: str
    animal_species: str
    is_neutering: bool
    animal_born_in: datetime
    animal_weight: float

    class Config:
        orm_mode = True

class PetUpdateRequest(Schema):
    animal_type: str
    is_neutering: str
    animal_born_in: datetime
    animal_weight: float

    class Config:
        orm_mode = True