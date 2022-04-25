# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-24 19:37:38
Message   : forms
'''
from email.mime import application
from lib2to3.pytree import Node
from django import forms
from tools import *

class ScholarForm(forms.Form):
    name = forms.CharField(label='学者姓名', max_length=30, required=True)
    acc_id = forms.CharField(label='学者id', max_length=10,required=False)
    email = forms.EmailField(label='邮箱', max_length=30, required=False)
    degree = forms.CharField(label='学位', max_length=30, required=False)
    field = forms.CharField(label='研究领域', widget=forms.Textarea, required=False)
    home_page = forms.URLField(label='学者主页', required=False)
    scholar_title = forms.CharField(label="学者头衔", required=False)
    work_unit = forms.CharField(label="工作地点", max_length=30, required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            pass
        else:
            raise forms.ValidationError('请输入正确的邮箱！')
        return email

    #检查论文格式
class PaperForm(forms.Form):
    name = forms.CharField(label='题目', max_length=100, required=True)
    author = forms.CharField(label='作者', max_length=100, required=True, initial='请逐个添加！')
    acc_id = forms.CharField(label='作者id', max_length=10, required=False)
    paper_source = forms.CharField(label='论文来源', max_length=50, required=False)

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if name_check(author) == 0:
            raise forms.ValidationError('该学者不存在，请先前往创建该节点！')
        return author
    
    def clean_acc_id(self):
        acc_id = self.cleaned_data.get('acc_id')
        if accid_check(acc_id) == 0:
            raise forms.ValidationError('请输入正确的作者id号!')
        return acc_id

class ProjectForm(forms.Form):
    name = forms.CharField(label='项目名字', max_length=100, required=True)
    acc_id = forms.CharField(label='作者id', max_length=10, required=False)
    participant = forms.CharField(label='参与者',max_length=100, required=True, initial='请逐个添加！')
    originAndId = forms.CharField(label='项目归属',max_length=100, required=False)
    application = forms.CharField(label='项目申请', max_length=100, required=True)
    
    def clean_acc_id(self):
        acc_id = self.cleaned_data.get('acc_id')
        if accid_check(acc_id) == 0:
            raise forms.ValidationError('请输入正确的作者id号!')
        return acc_id

    def clean_partition(self):
        partition = self.cleaned_data.get('partition')
        if name_check(partition) == 0:
            raise forms.ValidationError('该学者不存在，请先前往创建该节点！')
        return partition

class PaperNodeForm(PaperForm):
    acc_id = None
    author = None

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name_check(name) != 0:
            raise forms.ValidationError('该论文节点已经存在！')
        return name
            
class PaperRelForm(PaperForm):
    paper_source = None

class ProjectNodeForm(ProjectForm):
    acc_id = None
    participant = None

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name_check(name) != 0:
            raise forms.ValidationError('该项目节点已经存在！')
        return name

class ProjectRelForm(ProjectForm):
    originAndId = None
    application = None