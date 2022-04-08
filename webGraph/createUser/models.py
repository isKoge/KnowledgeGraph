# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-07 00:22:22
Message   : models
'''
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #org : 用户名
    org = models.CharField(verbose_name='Organization', max_length=128, blank=True)
    telephone = models.CharField(verbose_name='Telephone', max_length=11, blank=True)
    mod_data = models.DateTimeField('Last modified',auto_now=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'User profile'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return '{}'.format(self.user.__str__())
    