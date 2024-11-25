from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


class UserInfoResponse(BaseModel):
    user_id: str
    user_img: Literal["0", "1", "2", "3", "4", "5", "6"]


class UserCreateRequest(BaseModel):
    user_id: str
    # email: EmailStr
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    password: str  # password SecretStr 사용시 에러 발생! router에서 str()로 타입 변환해도 에러남
    # user_img: str

    class Config:
        # Pydantic에서 Django 모델을 사용할 때, 임의의 타입을 허용하도록 설정
        arbitrary_types_allowed = False


class UserLoginRequest(BaseModel):
    user_id: str
    password: str


class PasswordUpdateRequest(BaseModel):
    old_password: str
    new_password: str


class UserImgUpdateRequest(BaseModel):
    user_img: Literal["0", "1", "2", "3", "4", "5", "6"]
