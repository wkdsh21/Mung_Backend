from ninja import Router
from ninja.security import django_auth

from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout

from member.models import User
from member.schemas.users_schema import UserInfoResponse, UserCreateRequest, UserLoginRequest, PasswordUpdateRequest, UserImgUpdateRequest  # Pydantic 모델을 임포트

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

router = Router()

@router.get("/", auth=django_auth, response={200: UserInfoResponse})
def user_info(request: HttpRequest):
    return 200, {"user_id": request.auth.username, "user_img": request.auth.user_img}

# 회원가입 API
@router.post("/signup")
def signup(request, user: UserCreateRequest):
    # Pydantic 모델에서 validated_data를 가져와서 User 생성
    user_data = user.dict()  # Pydantic 모델에서 dict로 변환
    user = User.objects.create_user(
        username=user_data['user_id'],
        password=str(user_data['password']),
        # email=user_data['email'],
        # first_name=user_data['first_name'],
        # last_name=user_data['last_name'],
        # user_img=user_data['user_img'],
    )
    return 200, {"message": "회원가입이 성공적으로 처리되었습니다.", "user_id": user.id}

# @router.post("/login")            # sessionid 없고 로그인 유지 안되는 버전
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

# sessionid 발신과 로그인 유지 버전
@router.post("/login")
def login_view(request, login_user: UserLoginRequest):
    l_user = login_user.dict()
    user = authenticate(username=l_user["user_id"], password=l_user["password"])   # 사용자를 인증합니다.

    if user is not None:
        login(request, user)    # 인증된 사용자가 있다면 세션을 시작합니다.

        sessionid = request.session.session_key     # 세션 ID를 얻습니다.

        return 200, {"sessionid": sessionid}   # 세션 ID를 클라이언트에게 반환합니다.

    return 200, {"detail": "Invalid credentials"}

@router.get("/logout", auth=django_auth)
def user_logout(request: HttpRequest):
    logout(request)
    return 200, {"message": "로그아웃 되었습니다."}

@router.put("/pw_change", auth=django_auth)
def pw_change(request: HttpRequest, password: PasswordUpdateRequest):
    user = User.objects.get(username=request.auth.username)
    pw = password.dict()
    if user.check_password(pw["old_password"]):
        user.set_password(pw["new_password"])
        user.save()
        return 200, {"message": "비밀번호 변경이 성공적으로 처리되었습니다.", "status": "success"}
    return 202, {"message": "올바르지 않은 비밀번호 입니다.", "status": "fail"}

@router.put("/user_img_change", auth=django_auth)
def user_img_change(request: HttpRequest, image: UserImgUpdateRequest):
    user = User.objects.get(username=request.auth.username)
    user.user_img = image.user_img
    user.save()
    return 200, {"message": "유저 이미지 변경이 성공적으로 처리되었습니다.", "status": "success"}