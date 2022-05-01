# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-07 00:22:22
Message   : views
'''
from createUser.myforms import *
from createUser.models import UserProfile
from django.contrib.auth.models import User, UserManager
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            user = User.objects.create_user(username=username, password=password, email=email)

            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('users:index', args=[user.id]))
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form':form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
 
            user = auth.authenticate(username=username, password=password)
 
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:index', args=[user.id]))
                # return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
            else:
                # 登录失败
                return render(request, 'users/login.html', {'form': form, 'message':'请输入正确的密码 ！'})
    else:
        form = LoginForm()
 
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'users/profile.html', {'user': user, 'user_profile': user_profile})

@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        formPfd = ProfileForm(request.POST)

        if formPfd.is_valid():
            user.first_name = formPfd.cleaned_data['first_name']
            user.last_name = formPfd.cleaned_data['last_name']
            user.save()

            user_profile.org = formPfd.cleaned_data['org']
            user_profile.telephone = formPfd.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    else:
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'org': user_profile.org,
            'telephone': user_profile.telephone,
        }
        formPfd = ProfileForm(default_data)
    return render(request,'users/profile_update.html',{'formPfd': formPfd,'user': user})

@login_required
def index(request, pk):  # index页面需要一开始就加载的内容写在这里
	context = {}
	return render(request, 'kg/index.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login")
 
@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)
 
    if request.method == "POST":
        formPwd = PwdChangeForm(request.POST)
 
        if formPwd.is_valid():
            password = formPwd.cleaned_data['old_password']
            username = user.username
 
            user = auth.authenticate(username=username, password=password)
 
            if user is not None and user.is_active:
                new_password = formPwd.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect('/accounts/login/')
 
            else:
                return render(request, 'users/profile_update.html', {'form': formPwd,
                        'user': user, 'message': 'Old password is wrong Try again'})
    else:
        formPwd = PwdChangeForm()
 
    return render(request, 'users/profile_update.html', {'formPwd': formPwd, 'user': user})