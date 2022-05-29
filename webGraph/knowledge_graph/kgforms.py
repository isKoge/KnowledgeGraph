# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-24 19:37:38
Message   : forms
'''
from email.mime import application
from email.policy import default
from lib2to3.pytree import Node
from turtle import textinput
from django import forms
from tools import *

class ScholarForm(forms.Form):
    name = forms.CharField(label='学者姓名', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "小明"}))
    acc_id = forms.CharField(label='学者id', max_length=30,required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "123"}))
    email = forms.EmailField(label='邮箱', max_length=30, required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "123@123.com"}))
    degree = forms.CharField(label='学位', max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "博士"}))
    field = forms.CharField(label='研究领域', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "计算机科学与技术 , 软件工程 , 网络与信息安全"}))
    home_page = forms.URLField(label='学者主页', required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': "https://www.xxxx.com"}))
    scholar_title = forms.CharField(label="学者头衔", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "博士生导师"}))
    work_unit = forms.CharField(label="工作地点", max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "广东工业大学"}))
    
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if email_check(email):
    #         pass
    #     else:
    #         raise forms.ValidationError('请输入正确的邮箱！')
    #     return email

    #检查论文格式
class PaperForm(forms.Form):
    author = forms.CharField(label='作者', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "小明"}))
    acc_id = forms.CharField(label='作者id', max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "123"}))
    paper_id = forms.CharField(label='论文id', max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "123"}))
    name = forms.CharField(label='题目', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "基于知识图谱的学者资源管理系统"}))
    paper_source = forms.CharField(label='论文来源', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "广东工业大学"}))

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if name_check(author):
            pass
        else:
            raise forms.ValidationError('该学者不存在，请先前往创建该节点！')
        return author
    
    def clean_acc_id(self):
        acc_id = self.cleaned_data.get('acc_id')
        if accid_check(acc_id):
            pass
        else:
            raise forms.ValidationError('请输入正确的作者id号!')
        return acc_id

class ProjectForm(forms.Form):
    participant = forms.CharField(label='参与者',max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "小明"}))
    acc_id = forms.CharField(label='作者id', max_length=30, required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "123"}))
    name = forms.CharField(label='项目名字', max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "第16届亚运会信息发布系统咨询设计"}))
    originAndId = forms.CharField(label='项目归属',max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "第16届亚组委"}))
    application = forms.CharField(label='项目申请', max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "小明"}))
    
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if name_check(name):
    #         raise forms.ValidationError('该项目节点已经存在！')
    #     return name

    def clean_acc_id(self):
        acc_id = self.cleaned_data.get('acc_id')
        if accid_check(acc_id):
            pass
        else:
            raise forms.ValidationError('请输入正确的作者id号!')
        return acc_id

    def clean_participant(self):
        participant = self.cleaned_data.get('participant')
        if name_check(participant):
            pass
        else:
            raise forms.ValidationError('该学者不存在，请先前往创建该节点！')
        return participant

class PaperNodeForm(PaperForm):
    acc_id = None
    author = None
            
class PaperRelForm(PaperForm):
    paper_source = None
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name_check(name):
            pass
        else:
            raise forms.ValidationError('该论文节点不存在！')
        return name
    

class ProjectNodeForm(ProjectForm):
    acc_id = None
    participant = None

class ProjectRelForm(ProjectForm):
    originAndId = None
    application = None
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name_check(name):
            pass
        else:
            raise forms.ValidationError('该项目节点不存在！')
        return name

class SchoolNodeForm(forms.Form):
    name = forms.CharField(label='学校名称', max_length=30, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "广东工业大学"}))

class SchoolRelForm(forms.Form):
    nameScholar = forms.CharField(label='学者名字', max_length=100, required=True)
    acc_id = forms.CharField(label='学者id', max_length=30, required=False)
    nameSchool = forms.CharField(label='学校名称', max_length=30, required=True)

    def clean_nameScholar(self):
        nameScholar = self.cleaned_data.get('nameScholar')
        if name_check(nameScholar):
            pass
        else:
            raise forms.ValidationError('学者节点不存在！')
        return nameScholar
    
    def clean_acc_id(self):
        acc_id = self.cleaned_data.get('acc_id')
        if accid_check(acc_id):
            pass
        else:
            raise forms.ValidationError('请输入正确的作者id号!')
        return acc_id
    
    def clean_nameSchool(self):
        nameSchool = self.cleaned_data.get('nameSchool')
        if name_check(nameSchool):
            pass
        else:
            raise forms.ValidationError('学校节点不存在！')
        return nameSchool

class RelForm(forms.Form):

    a = 'Author_of_paper'
    b = 'Author_of_project'
    c = 'work_for_school'
    RELTYPE_CHOICES = [
        (a,'论文作者'),
        (b,'项目参与者'),
        (c,'工作地点')
    ]
    ScholarName = forms.CharField(label='学者名字', max_length=100, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':"学者姓名"}))
    acc_id = forms.CharField(label='学者id', max_length=30, required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':"学者id"}))
    relType = forms.ChoiceField(choices=RELTYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control','placeholder':"类型"}))
    nodeName = forms.CharField(label='节点名称', max_length=30, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':"学术成就"}))
    message = forms.CharField(label='其他信息', max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':"其它信息"}))


    # def clean_ScholarName(self):
    #     ScholarName = self.cleaned_data.get('ScholarName')
    #     if name_check(ScholarName):
    #         pass
    #     else:
    #         raise forms.ValidationError('学者节点不存在！')
    #     return ScholarName
    
    # def clean_acc_id(self):
    #     acc_id = self.cleaned_data.get('acc_id')
    #     if accid_check(acc_id):
    #         pass
    #     else:
    #         raise forms.ValidationError('请输入正确的作者id号!')
    #     return acc_id
    
    def clean_nodeName(self):
        nodeName = self.cleaned_data.get('nodeName')
        if name_check(nodeName):
            pass
        else:
            raise forms.ValidationError('节点不存在！')
        return nodeName 