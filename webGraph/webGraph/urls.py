# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-05 15:47:59
Message   : 
'''
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('createUser.urls','users'))
]
