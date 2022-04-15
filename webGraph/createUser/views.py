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
            return HttpResponseRedirect('/accounts/login')
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form':form})

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
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    else:
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'org': user_profile.org,
            'telephone': user_profile.telephone,
        }
        form = ProfileForm(default_data)
    return render(request,'users/profile_update.html',{'form': form,'user': user})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
 
            user = auth.authenticate(username=username, password=password)
 
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
            else:
                # 登录失败
                return render(request, 'users/login.html', {'form': form, 'message':'Wrong password Please Try agagin'})
    else:
        form = LoginForm()
 
    return render(request, 'users/login.html', {'form': form})
 
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")
 
@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)
 
    if request.method == "POST":
        form = PwdChangeForm(request.POST)
 
        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username
 
            user = auth.authenticate(username=username, password=password)
 
            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect('/accounts/login/')
 
            else:
                return render(request, 'users/pwd_change.html', {'form': form,
                        'user': user, 'message': 'Old password is wrong Try again'})
    else:
        form = PwdChangeForm()
 
    return render(request, 'users/pwd_change.html', {'form': form, 'user': user})