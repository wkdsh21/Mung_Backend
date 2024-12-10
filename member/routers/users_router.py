import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import redirect
from ninja import Router
from ninja.security import django_auth
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from config import settings
from member.models import User
from member.schemas.users_schema import (
    PasswordUpdateRequest,
    UserCreateRequest,
    UserDeleteRequest,
    UserImgUpdateRequest,
    UserInfoResponse,
    UserLoginRequest,
)

router = Router(tags=["users"])


@router.get("/", auth=django_auth, response={200: UserInfoResponse})
def user_info(request: Request) -> tuple[int, dict[str, str]]:
    user = request.user
    return 200, {"user_id": user.username, "user_img": getattr(user, "user_img", "")}


# 회원가입 API
@router.post("/signup", response={201: dict, 409: dict})
def signup(request: HttpRequest, user: UserCreateRequest) -> tuple[int, dict[str, str]]:
    if User.objects.filter(username=user.user_id).exists():
        return 409, {"message": "이미 가입된 유저입니다.", "status": "failed"}
    # Pydantic 모델에서 validated_data를 가져와서 User 생성
    user_data = user.dict()  # Pydantic 모델에서 dict로 변환
    User.objects.create_user(
        username=user_data["user_id"],
        password=str(user_data["password"]),
        # email=user_data['email'],
        # first_name=user_data['first_name'],
        # last_name=user_data['last_name'],
        # user_img=user_data['user_img'],
    )
    return 201, {"message": "회원가입이 성공적으로 처리되었습니다.", "status": "success"}

@router.get("/social/kakao/login")
def kakao_social_login(request):
    return redirect(
        "https://kauth.kakao.com/oauth/authorize"
        f"?client_id={settings.KAKAO_REST_API_KEY}"
        f"&redirect_uri={settings.KAKAO_REDIRECT_URL}"
        f"&response_type=code",     # callback: authrization_code
    )

@router.get(
    "/social/kakao/callback",
    response={201: dict, 409: dict},
)
def kakao_social_callback(request):

    user_token = request.GET.get("code")
    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token"
        f"?grant_type=authorization_code&client_id={settings.KAKAO_REST_API_KEY}"
        f"&redirect_uri={settings.KAKAO_REDIRECT_URL}"
        f"&code={user_token}",
        {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    )

    token_response_json = token_request.json()
    print(token_response_json)
    error = token_response_json.get("error", None)
    if error:
        return 409, {"message": error, "status": "failed"}
    access_token = token_response_json.get("access_token")

    profile_request = requests.get(
        f"https://kapi.kakao.com/v2/user/me",
        {"Authorization": f"Bearer {access_token}"}
    )

    profile_json = profile_request.json()
    print(profile_json)
    user_subject = str(profile_json["id"])
    email = profile_json["kakao_account"]["email"]



    #
    #     profile_response.raise_for_status()
    #     if profile_response.is_success:
    #         # 3) 사용자 정보 -> 회원가입/로그인
    #         member_profile: dict = profile_response.json()
    #         member_subject: str = str(member_profile["id"])
    #
    #         email: str = profile_response.json()["kakao_account"]["email"]
    #         member: Member | None = member_repo.get_member_by_social_email(
    #             social_provider=SocialProvider.KAKAO,
    #             email=email
    #         )
    #
    #         if member:  # 이미 가입된 사용자 -> 로그인
    #             return JWTResponse(access_token=encode_access_token(username=member.username))
    #         new_member = Member.social_signup(
    #             social_provider=SocialProvider.KAKAO,
    #             subject=member_subject,
    #             email=email,
    #         )
    #         member_repo.save(new_member)
    #
    #         return JWTResponse(
    #             access_token=encode_access_token(username=new_member.username),
    #         )
    #
    # raise HTTPException(
    #     status_code=status.HTTP_400_BAD_REQUEST,
    #     detail="Kakao social login failed",
    # )

# sessionid 발신과 로그인 유지 버전
@router.post("/login", response={200: dict, 400: dict})
def login_view(request: HttpRequest, login_user: UserLoginRequest) -> tuple[int, dict[str, str]]:
    l_user = login_user.dict()
    user = authenticate(username=l_user["user_id"], password=l_user["password"])  # 사용자를 인증합니다.

    if user is not None:
        login(request, user)  # 인증된 사용자가 있다면 세션을 시작합니다.

        sessionid = request.session.session_key  # 세션 ID를 얻습니다.

        return 200, {"sessionid": str(sessionid)}  # 세션 ID를 클라이언트에게 반환합니다.

    return 400, {"detail": "잘못된 아이디 혹은 비밀번호"}


@router.get("/logout", auth=django_auth, response={200: dict})
def user_logout(request: HttpRequest) -> tuple[int, dict[str, str]]:
    logout(request)
    return 200, {"message": "로그아웃 되었습니다."}


@router.put("/pw_change", auth=django_auth, response={200: dict, 401: dict})
def pw_change(request: HttpRequest, password: PasswordUpdateRequest) -> tuple[int, dict[str, str]]:
    user = User.objects.get(username=request.user)
    pw = password.dict()
    if user.check_password(pw["old_password"]):
        user.set_password(pw["new_password"])
        user.save()
        return 200, {
            "message": "비밀번호 변경이 성공적으로 처리되었습니다.",
            "status": "success",
        }
    return 401, {"message": "올바르지 않은 비밀번호 입니다.", "status": "fail"}


@router.put("/img_change", auth=django_auth, response={200: dict})
def user_img_change(request: HttpRequest, image: UserImgUpdateRequest) -> tuple[int, dict[str, str]]:
    user = User.objects.get(username=request.user)
    user.user_img = image.user_img
    user.save()
    return 200, {"message": "유저 이미지 변경이 성공적으로 처리되었습니다.", "status": "success"}


@router.delete("/", auth=django_auth, response={200: dict, 401: dict})
def delete_user(request: HttpRequest, pw: UserDeleteRequest) -> tuple[int, dict[str, str]]:
    user = User.objects.get(username=request.user)
    if user.check_password(pw.password):
        user.delete()
        logout(request)
        return 200, {
            "message": "회원탈퇴가 성공적으로 처리되었습니다.",
            "status": "success",
        }
    return 401, {"message": "올바르지 않은 비밀번호 입니다.", "status": "fail"}
