# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-05 15:47:59
Message   : 
'''
from django.contrib import admin
from django.urls import path, include
from knowledge_graph import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('createUser.urls','users')),
    path('kg/', include('knowledge_graph.urls', 'kg'))
]
