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
    username = forms.CharField(label='Username', max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "用户名"}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "邮箱"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "密码"}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "确认密码"}))

    # 检查 usernmae 是否合法,包括长度，是否存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('用户名不能少于3位！')
        elif len(username) > 20:
            raise forms.ValidationError('用户名最多20位！')
        else:
            filter_result =User.objects.filter(username__exact=username)
            if filter_result:
                raise forms.ValidationError('用户名已经存在！')
        return username
    
    # 检查 email 是否合法，是否存在
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email__exact = email)
            if filter_result:
                raise forms.ValidationError('邮箱已经存在！')
        else:
            raise forms.ValidationError('请检查邮箱格式！')
        return email

    #检查 password 是否合格
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 3:
            raise forms.ValidationError('密码不能少于3位！')
        elif len(password1) > 20:
            raise forms.ValidationError('密码不能超过20位！')
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次密码不一致！')
        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "用户名",'autofocus': '', 'style':"margin:10px 0px"}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "密码",'style':"margin:10px 0px"}))

    # 使用邮箱登录或用户名登录时候，判断是否存在或正确
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if email_check(username):
            filter_result = User.objects.filter(email__exact = username)
            if not filter_result:
                raise forms.ValidationError('请输入正确的邮箱！')
        else:
            filter_result = User.objects.filter(username__exact = username)
            if not filter_result:
                raise forms.ValidationError('请输入正确的用户名！')
        return username
        
class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "姓"}))
    last_name = forms.CharField(label='Last Name', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "名"}))
    org = forms.CharField(label='Organization', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "组织"}))
    telephone = forms.CharField(label='Telephone',max_length=11, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "电话"}))

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone_check(telephone):
            return telephone
        else:
            raise forms.ValidationError('请输入合理的电话！')

class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入旧密码！"}))
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入新密码！"}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请确认新密码！"}))

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError('密码不能低于6位！')
        elif len(password1) > 20:
            raise forms.ValidationError('密码不能超过20位！')
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次密码不一致！')
        return password2


        
