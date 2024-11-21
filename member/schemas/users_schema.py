from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateSchema(BaseModel):
    username: str
    # email: EmailStr
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    password: str
    # user_img: str

    class Config:
        # Pydantic에서 Django 모델을 사용할 때, 임의의 타입을 허용하도록 설정
        arbitrary_types_allowed = False
