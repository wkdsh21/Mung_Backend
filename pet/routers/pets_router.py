from datetime import datetime
from xmlrpc.client import DateTime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from pet.schemas.pets_schema import PetCreateRequest, PetGetListResponse, PetUpdateRequest
from pet.models import Pets

router = Router()

@router.get("/", response={200: list[PetGetListResponse]})
def get_pets_list(request: HttpRequest) -> tuple[int, list[Pets]]:
    pets = Pets.objects.filter(user=request.user)
    return 200, [pet for pet in pets]


@router.post("/")
def create_pet(request: HttpRequest, pet_request: PetCreateRequest) -> int:
    Pets.objects.create(
        **pet_request.dict()
    )
    return 201


@router.put("/{id}")
def update_pet(request: HttpRequest, pet_request: PetUpdateRequest, id: int) -> int:
    Pets.objects.filter(user=request.user, pet_id=id).update(
        **pet_request.dict()
    )
    return 200
