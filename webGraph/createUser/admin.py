# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-07 00:22:22
Message   : 
'''
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
class UserProFileAdmin(UserAdmin):
    inlines = [UserProfileInline,]

admin.site.register(User, UserProFileAdmin)