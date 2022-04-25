# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-14 15:21:24
Message   : 
'''
from django.shortcuts import render
from knowledge_graph.models import Neo4j
import json
from django.contrib.auth.decorators import login_required
from knowledge_graph.kgforms import *

# 链接 Neo4j 
neo_con = Neo4j()
neo_con.connectDB()

# 初始页面
@login_required
def index(request):  # index页面需要一开始就加载的内容写在这里
	context = {}
	return render(request, 'kg/index.html', context)

@login_required
def search_relation(request):
	ctx = {}
	db = neo_con
	if(request.GET):
		ctx= {'title' : '<h1>暂未找到相应的匹配</h1>'}
		
		entity1 = request.GET['entity1_text']
		relation = request.GET['relation_name_text']
		entity2 = request.GET['entity2_text']
		searchResult = {}

		#若只输入entity1,则输出与entity1有直接关系的实体和关系
		if(len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0):
			searchResult = db.findRelationByEntity1(entity1)
			if(len(searchResult)>0):
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				return render(request,'kg/relation.html',{'ctx':ctx}) 

		#若只输入entity2则,则输出与entity2有直接关系的实体和关系
		if(len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0):
			searchResult = db.findRelationByEntity2(entity2)
			if(len(searchResult)>0):
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				return render(request,'kg/relation.html',{'ctx':ctx})

		#若输入entity1和relation，则输出与entity1具有relation关系的其他实体
		if(len(entity1)!=0 and len(relation)!=0 and len(entity2) == 0):
			searchResult = db.findOtherEntities(entity1,relation)
			if(len(searchResult)>0):
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				return render(request,'kg/relation.html',{'ctx':ctx})

		#若输入entity2和relation，则输出与entity2具有relation关系的其他实体
		if(len(entity2)!=0 and len(relation)!=0 and len(entity1) == 0):
			searchResult = db.findOtherEntity2(entity2,relation)
			if(len(searchResult)>0):
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				return render(request,'kg/relation.html',{'ctx':ctx})

		#若输入entity1和entity2,则输出entity1和entity2之间的最短路径
		if(len(entity1) !=0 and len(relation) == 0 and len(entity2)!=0):
			searchResult = db.findRelationByEntities(entity1,entity2)
			if(len(searchResult)>0):
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				return render(request,'kg/relation.html',{'ctx':ctx})

		#全为空 则输出整个知识图谱
		if(len(entity1)==0 and len(relation)==0 and len(entity2) ==0 ):
			searchResult =db.zhishitupu()
			#print(json.loads(json.dumps(searchResult)))
			return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

	return render(request,'kg/relation.html',{'ctx':ctx}) 

@login_required
def Node_update(request):
	db = neo_con 
	if request.method == 'POST':
		select_type = request.POST.get('select_type')
		node_type = ''
		if select_type == '学者':
			form = ScholarForm(request.POST)
			node_type = 'scholar'

		elif select_type == '论文':
			form = PaperNodeForm(request.POST)
			node_type = 'paper'

		elif select_type == '项目':
			form = ProjectNodeForm(request.POST)
			node_type = 'project'

		if form.is_valid():
			message = form.cleaned_data
			db.createNode(node_type, message)

	else:
		form_scholar = ScholarForm()
		form_paper = PaperNodeForm()
		form_project = ProjectNodeForm()
	return render(request, 'kg/Nodeupdate.html', {'form_scholar': form_scholar, 'form_paper': form_paper, 'form_project': form_project})


def Rel_update(request):
	pass