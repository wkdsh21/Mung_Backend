from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.security import django_auth

from pet.schemas.pets_schema import PetCreateRequest, PetGetListResponse, PetUpdateRequest
from pet.models import Pets

router = Router()

@router.get("/", response={200: list[PetGetListResponse]}, auth=django_auth)
def get_pets_list(request: HttpRequest) -> tuple[int, list[Pets]]:
    pets = Pets.objects.filter(user=request.user)
    return 200, [pet for pet in pets]


@router.post("/", auth=django_auth)
def create_pet(request: HttpRequest, pet_request: PetCreateRequest) -> int:
    obj=Pets.objects.create(
        **pet_request.dict(),
        user=request.user,
        pet_id = request.user.pet_cnt + 1
    )
    if obj:
        request.user.pet_cnt += 1
        request.user.save()
    return 201


@router.put("/{id}", auth=django_auth)
def update_pet(request: HttpRequest, pet_request: PetUpdateRequest, id: int) -> int:
    pet = Pets.objects.filter(user=request.user, pet_id=id)
    if pet.exists():
        pet.update(
        **pet_request.dict()
        )
    else:
        raise Http404
    return 200

@router.delete("/{id}", auth=django_auth)
def delete_pet(request: HttpRequest, id: int) -> int:
    pet = Pets.objects.filter(pet_id=id,user=request.user)
    if pet.exists() and pet.delete()[0] == 1:
        request.user.pet_cnt -= 1
        request.user.save()
    else:
        raise Http404
    return 200
