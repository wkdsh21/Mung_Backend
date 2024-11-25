from datetime import date, datetime

from django.db.models import ProtectedError
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.security import django_auth

from member.models import User
from pet.models import Pets, PetsWeights
from pet.schemas.pets_schema import (
    PetCreateRequest,
    PetGetCardResponse,
    PetGetGraphResponse,
    PetGetListResponse,
    PetUpdateRequest,
)

router = Router()


@router.get("/", response={200: list[PetGetListResponse]}, auth=django_auth)
def get_pets_list(request: HttpRequest) -> tuple[int, list[Pets]]:
    user = request.user
    assert isinstance(user, User)
    pets = Pets.objects.filter(user_id=user.id)
    return 200, [pet for pet in pets]


@router.post("/", response={201: dict}, auth=django_auth)
def create_pet(request: HttpRequest, pet_request: PetCreateRequest) -> tuple[int, dict[str, str]]:
    user = request.user
    assert isinstance(user, User)
    obj = Pets.objects.create(**pet_request.dict(), user_id=user.id)
    if obj:
        user.pet_cnt += 1
        user.save()
        PetsWeights.objects.create(weight=obj.weight, pet=obj)
    return 201, {
        "message": "애완동물이 성공적으로 등록되었습니다.",
        "status": "success",
    }


@router.put("/{int:id}", response={200: dict}, auth=django_auth)
def update_pet(request: HttpRequest, pet_request: PetUpdateRequest, id: int) -> tuple[int, dict[str, str]]:
    user = request.user
    assert isinstance(user, User)
    pet = get_object_or_404(Pets, user_id=user.id, id=id)
    for key, value in pet_request.dict().items():
        setattr(pet, key, value)
    pet.save()
    try:
        pet_weights = PetsWeights.objects.get(pet=pet, last_modified_at__date=date.today())
        pet_weights.weight = pet.weight
        pet_weights.save()  # save시에만 auto_now 동작
    except PetsWeights.DoesNotExist:
        PetsWeights.objects.create(weight=pet.weight, pet=pet)
    return 200, {"message": "동물 수정이 성공하였습니다.", "status": "success"}


@router.delete("/{int:id}", response={200: dict}, auth=django_auth)
def delete_pet(request: HttpRequest, id: int) -> tuple[int, dict[str, str]]:
    user = request.user
    assert isinstance(user, User)
    pet = get_object_or_404(Pets, id=id, user_id=user.id)
    try:
        pet.delete()
    except ProtectedError:
        return 409, {
            "message": "Cannot delete this object because it is referenced by another object.",
            "status": "error",
        }
    return 200, {"message": "동물 삭제가 성공하였습니다.", "status": "success"}


@router.get("/card", response={200: list[PetGetCardResponse]}, auth=django_auth)
def get_pets_card(request: HttpRequest) -> tuple[int, list[Pets]]:
    user = request.user
    assert isinstance(user, User)
    pets = Pets.objects.filter(user_id=user.id)
    return 200, [pet for pet in pets]


@router.get("/graph/{int:id}", response={200: list[PetGetGraphResponse]}, auth=django_auth)
def get_pets_graph(request: HttpRequest, id: int) -> tuple[int, list[PetsWeights]]:
    # 유저랑 pet 연결해서 찾아와야됨 아마 model 스키마 변경해야할듯
    user = request.user
    assert isinstance(user, User)
    pet = get_object_or_404(Pets, user_id=user.id, id=id)
    graphs = PetsWeights.objects.filter(pet_id=pet.id)
    return 200, [graph for graph in graphs]
