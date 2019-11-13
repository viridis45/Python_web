from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm #UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model




def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
        pass
    else:
        form = CustomUserCreationForm()
    context= {'form':form}
    return render(request, 'accounts/auth_form.html', context)




def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
            # get_user는 user-cache의 클래스 멤버변수를 리턴하는 메서드
            # 처음에는 아무것도 없다가 is_valid가 호출된상테에는 cleaned data가 호출되어 user_cache에 담기게 됨
            # 이를 가져오는 변수가 get_user()

    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_POST
def delete(request):
    request.user.delete()
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance = request.user)
    context = {'form':form}
    return render(request, 'accounts/auth_form.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) 
            # 현재 사용자의 인증 세션이 무효화 되는것을 막고
            # 세션을 유지한 상태로 비밀번호를 업데이트 시켜준다

            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'accounts/auth_form.html', context)


def profile(request, username):
    # user모델을 가져오는 두 가지 방법
    # 1. get_user_model() = 객체반환 (model.py  제외 전부)
    # 2. srttings.AUTH_USER_MODEL - 스트링 반환 (model.py)
    person = get_object_or_404(get_user_model(), username=username)
    context = {'person': person}
    return render(request, 'accounts/profile.html', context)
