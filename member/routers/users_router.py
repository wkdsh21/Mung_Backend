from ninja import Router
from ninja.security import django_auth

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login

from member.models import User
from member.schemas.users_schema import UserCreateSchema  # Pydantic 모델을 임포트

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

router = Router()

@router.get("/", auth=django_auth)
def user_info(request: HttpRequest):
    return {"user_id": request.auth.username, "user_img": request.auth.user_img}

# 회원가입 API
@router.post("/signup")
def signup(request, user: UserCreateSchema):
    # Pydantic 모델에서 validated_data를 가져와서 User 생성
    user_data = user.dict()  # Pydantic 모델에서 dict로 변환
    user = User.objects.create_user(
        username=user_data['username'],
        password=user_data['password'],
        # email=user_data['email'],
        # first_name=user_data['first_name'],
        # last_name=user_data['last_name'],
        # user_img=user_data['user_img'] or "0",
    )
    return {"message": "회원가입이 성공적으로 처리되었습니다.", "user_id": user.id}

# @router.post("/login")
# def login(request, username: str, password: str):
#
#     # 인증
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         # JWT 토큰 발급
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         return {"access_token": access_token, "refresh_token": str(refresh)}
#     return {"detail": "Invalid credentials"}, 422

@router.post("/login")
def login_view(request, username: str, password: str):
    # 사용자를 인증합니다.
    user = authenticate(username=username, password=password)

    if user is not None:
        # 인증된 사용자가 있다면 세션을 시작합니다.
        login(request, user)

        # 세션 ID를 얻습니다.
        sessionid = request.session.session_key

        # 세션 ID를 클라이언트에게 반환합니다.
        return JsonResponse({"sessionid": sessionid}, status=200)

    return JsonResponse({"detail": "Invalid credentials"}, status=422)