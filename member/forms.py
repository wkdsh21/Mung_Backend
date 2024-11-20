# member/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User  # 커스터마이즈한 User 모델

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # 기존의 User 모델이 아닌, member.User 모델을 지정
        fields = ('username', 'user_img')  # 필요한 필드만 추가하거나 수정

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User