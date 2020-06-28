from django.contrib.auth import logout, update_session_auth_hash, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import UserForm


# minha conta
def account(request):
    return render(request, 'account/account.html', locals())
    

# adicionar usuário
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            u = form.save()
            u.set_password(u.password)
            u.username = u.email
            u.save()
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, 'account/register.html', locals())

# login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'account/login.html', locals())

# alterar senha
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', locals())

# logout
def user_logout(request):
    logout(request)
    return redirect('/')
