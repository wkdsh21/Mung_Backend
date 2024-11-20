# # from django.contrib.auth.hashers import check_password
# # from django.contrib.auth.models import User
# # # from account.models import User
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.contrib.auth import login as django_login, update_session_auth_hash
# from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
#
# def sign_up(request):
#     form = CustomUserCreationForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('/users/login/')
#
#     context = {'form': form}
#     return render(request, 'registration/signup.html', context)
#
# def login(request):
#     form = CustomAuthenticationForm(request, request.POST or None)
#     if form.is_valid():
#         # django_login(request, form.get_user())
#         # print(request.session.keys())
#         # print(request.session.values())
#         context = {"session": request.session['_auth_user_hash']}
#         return render(request, 'main_page.html', context)
#
#     return render(request, 'registration/login.html', {'form': form})
#
# def change_password(request):
#     form = CustomPasswordChangeForm(request.user, request.POST or None)
#     if form.is_valid():
#         user = form.save()
#         # update_session_auth_hash(request, user)   # 활성화하면 비밀번호 변경 후에도 로그인이 상태가 해제되지 않는다
#         return redirect('/')
#     else:
#         messages.error(request, 'Please correct the error below.')
#
#     return render(request, 'registration/change_password.html', {'form': form})