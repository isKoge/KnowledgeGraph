# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-14 15:48:53
Message   : 
'''
from django.urls import re_path
from knowledge_graph.views import *
app_name = 'kg'

urlpatterns = [
    re_path(r'^search_relation',search_relation, name='search_relation'),
    re_path(r'^NodeManage',NodeManage, name='Node_update'),
    re_path(r'^RelManage',RelManage, name='RelManage'),
    re_path(r'^js',jsReturn, name='jsReturn'),
    re_path(r'^all',all, name='all')
]