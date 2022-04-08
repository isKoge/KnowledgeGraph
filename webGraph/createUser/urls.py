# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-08 08:42:05
Message   : 
'''
from createUser.views import *
from django.urls import re_path

app_name = 'users'

urlpatterns = [
    re_path(r'^register/$', register, name='register'),
    re_path(r'^login/$', login, name='login'),
    re_path(r'^user/(?P<pk>\d+)/profile/$', profile, name='profile'),
    re_path(r'^user/(?P<pk>\d+)/profile/update/$', profile_update, name='profile_update'),
    re_path(r'^user/(?P<pk>\d+)/pwd_change/$', pwd_change, name='pwd_change'),
    re_path(r"^logout/$", logout, name='logout'),
]
