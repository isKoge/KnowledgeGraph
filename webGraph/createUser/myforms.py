# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-08 08:42:19
Message   : forms 
'''
from tools import *
from django import forms
from django.contrib.auth.models import User

# 检查邮箱是否合法
def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

# 检查电话是否合法
def telephone_check(telephone):
    pattern = re.compile(r'^(13[0-9]|15[0123456789]|18[0-9]|14[57])[0-9]{8}$')
    return re.match(pattern, telephone)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # 检查 usernmae 是否合法,包括长度，是否存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters log !')
        elif len(username) > 20:
            raise forms.ValidationError('Username is too long !')
        else:
            filter_result =User.objects.filter(username__exact=username)
            if filter_result:
                raise forms.ValidationError('Username already exists !')
        return username
    
    # 检查 email 是否合法，是否存在
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email__exact = email)
            if filter_result:
                raise forms.ValidationError('Email already exists !')
        else:
            raise forms.ValidationError('Please enter a valid email !')
        return email

    #检查 password 是否合格
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 3:
            raise forms.ValidationError('Password is too short !')
        elif len(password1) > 20:
            raise forms.ValidationError('Password is too long !')
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords are inconsistent !')
        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    # 使用邮箱登录或用户名登录时候，判断是否存在或正确
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if email_check(username):
            filter_result = User.objects.filter(email__exact = username)
            if not filter_result:
                raise forms.ValidationError('Please enter the correct Email !')
        else:
            filter_result = User.objects.filter(username__exact = username)
            if not filter_result:
                raise forms.ValidationError('Please enter the correct Username !')
        return username
        
class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    org = forms.CharField(label='Organization', max_length=50, required=False)
    telephone = forms.CharField(label='Telephone',max_length=11, required=False)

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone_check(telephone):
            return telephone
        else:
            raise forms.ValidationError('Please enter a valid Telephone !')

class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)

    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError('Password is too short !')
        elif len(password1) > 20:
            raise forms.ValidationError('Password is too long !')
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords are inconsistent !')
        return password2


        
