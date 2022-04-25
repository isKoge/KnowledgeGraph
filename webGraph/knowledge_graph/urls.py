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
    re_path(r'^Node_update',Node_update, name='Node_update'),
    # re_path(r'^Rel_update',Rel_update, name='Rel_update')
]
