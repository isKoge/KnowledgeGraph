# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-14 15:21:24
Message   : 
'''
from django.http import HttpResponse
from django.shortcuts import render
from knowledge_graph.models import Neo4j
import json
from django.contrib.auth.decorators import login_required
from knowledge_graph.kgforms import *
from django.views.decorators.csrf import csrf_exempt

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
			searchResult = db.zhishitupu()
			#print(json.loads(json.dumps(searchResult)))
			return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		#如输入两个学者查看合作节点
		if relation == 'cooperation':
			n1 = {'name':entity1}
			n2 = {'name':entity2}
			searchResult = db.findRelBy2Node(n1,n2,'scholar','scholar')
			if len(searchResult) > 0:
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
				
	return render(request,'kg/relation.html',{'ctx':ctx})

def selectForm(formType, select_type):
	if formType == 'n':
		if select_type == 1:
			form = ScholarForm()
		elif select_type == 2:
			form = PaperNodeForm()
		elif select_type == 3:
			form = ProjectNodeForm()
		elif select_type == 4:
			form = SchoolNodeForm()
	elif formType == 'r':
		form = RelForm()
	return form


@login_required
def NodeManage(request):
	db = neo_con 
	message = {}
	if request.method == 'POST':
		# 选择当前是什么种类，1学者，2论文，3项目
		select_type = request.POST.get('select_type')
		# 选择功能，1增加，2删除，3查找, 4修改
		select_fun = request.POST.get('select_fun')
		node_type = ''
		if select_type == 1:
			form = ScholarForm(request.POST)
			node_type = 'scholar'
		elif select_type == 2:
			form = PaperNodeForm(request.POST)
			node_type = 'paper'
		elif select_type == 3:
			form = ProjectNodeForm(request.POST)
			node_type = 'project'
		else:
			form = SchoolNodeForm(request.POST)
			node_type = 'school'

		if form.is_valid():
			node_message = form.cleaned_data
			node_name = form.cleaned_data.get('name')
			if select_fun == 1:
				if db.createNode(node_type, **node_message):
					message = '添加节点成功！'
					form = selectForm('n',select_type)
					return render(request,'kg/NodeMange.html',{'form':form, 'message':message})
				else:
					message = '添加节点失败，节点已经存在！'
					return render(request,'kg/NodeMange.html',{'form':form, 'message':message})
			elif select_fun == 2:
				answer = db.delNode(node_type, **node_message)
				if answer:
					if answer == 1:
						message = '删除节点成功！'
						form = selectForm('n',select_type)
						return render(request,'kg/NodeMange.html',{'form':form, 'message':message})
					else:
						message = '节点存在多个，请选择其中一个！'
						searchResult = list(db.findByNode(node_type, **node_message))
						return render(request,'kg/NodeManage.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False),'message':message})
				else:
					message = '删除节点失败，节点不存在！'
					return render(request,'kg/NodeMange.html',{'form':form, 'message':message})
			elif select_fun == 3:
				answer = db.findByNode(node_type, **node_message)
				if answer:
					message = '查找成功！'
					searchResult = list(answer)
					return render(request,'kg/NodeManage.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False),'message':message})
				else:
					message = '不存在节点！'
					return render(request,'kg/NodeMange.html',{'message':message})
			else:
				answer = db.updateNode(node_message, node_type, name=node_name)
				if answer:
					if answer == 1:
						message = '修改成功！'
						return render(request,'kg/NodeMange.html',{'form':form, 'message':message})
					else:
						message = '节点存在多个，请选择其中一个！'
						searchResult = list(db.findByNode(node_type, **node_message))
						return render(request,'kg/NodeManage.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False),'message':message})
				else:
					message = '修改失败！'
					return render(request, 'kg/NodeManage.html', {'form': form, 'message':message})
	else:
		formScholar = ScholarForm()
		formPaper = PaperNodeForm()
		formProject = ProjectNodeForm()
		formSchool = SchoolNodeForm()
	return render(request, 'kg/NodeManage.html', {'formScholar':formScholar, 'formPaper':formPaper, 'formProject':formProject, 'formSchool':formSchool})

@login_required
def RelManage(request):
	db = neo_con
	message = {}
	if request.method == 'POST':
		# 1.学者->论文(paper) ，2.学者->项目(project)，3.学者->学校(school)
		# 选择功能，1增加，2删除，3查找
		form = RelForm(request.POST)
		select_fun = request.POST.get('select_fun')
		# papaerRel: author, accid, name
		# projectRel: participant, accid, name
		# schoolRel: nameScholar, accid. nameSchool
		if form.is_valid():
			select_type = form.cleaned_data.get('relType')
			scholarNode = form.cleaned_data.get('ScholarName')
			scholarAccid = form.cleaned_data.get('acc_id')
			toNode = form.cleaned_data.get('nodeName')
			message = form.cleaned_data.get('message')
			if scholarAccid:
				n1_key = {'name':scholarNode,'acc_id':scholarAccid}
			else:
				n1_key = {'name':scholarNode}
			n2_key = {'name':toNode}
		
			if select_fun == 1:
				answer = db.createRel('scholar',n1_key,n2_type=None,n2_key=n2_key, message=message)
				if answer:
					message = '添加关系成功！'
					form = selectForm('r',select_type)
					return render(request,'kg/RelMange.html',{'form':form, 'message':message})
				else:
					message = '添加关系失败！'
					return render(request,'kg/RelMange.html',{'form':form, 'message':message})

			elif select_fun == 2:
				answer = db.delRel(n1_key,n2_key,'scholar',n2_type=None)
				if answer:
					if answer == 1:
						message = '删除关系成功！'
						form = selectForm('r',select_type)
						return render(request,'kg/RelMange.html',{'form':form, 'message':message})
					elif answer == 2:
						message = '同名学者存在多个，请选择其中一个！'
						searchResult = list(db.findByNode(node_type='scholar',**n1_key))
						return render(request,'kg/RelManage.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False),'message':message})
					else:
						message = '同名节点存在多个，请选择其中一个！'
						searchResult = list(db.findByNode(node_type=None,**n2_key))
						return render(request,'kg/RelManage.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False),'message':message})
				else:
					message = '删除关系失败，关系不存在！'
					return render(request,'kg/RelMange.html',{'form':form, 'message':message})
			else:
				answer = db.findRelBy2Node(n1_key,n2_key,'scholar')
				if answer:
					message = '关系查找成功！'
					searchResult = list(answer)
					return render(request,'kg/RelManage.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False),'message':message})
				else:
					message = '不存在节点！'
					return render(request,'kg/RelMange.html',{'message':message})
		else:
			pass
	else:
		form = RelForm()
	return render(request, 'kg/RelManage.html', {'form':form})

#前端点击返回数据
@csrf_exempt
def jsReturn(request):
	db = neo_con
	nodeName = request.POST.get('data')
	nodeType = request.POST.get('style')

	if nodeType == '0':
		searchResult = db.findByNode(node_type='scholar', name=nodeName)
	elif nodeType == '1':
		searchResult = db.findByNode(node_type='paper', name=nodeName)
	elif nodeType == '2':
		searchResult = db.findByNode(node_type='project', name=nodeName)
	else:
		searchResult = db.findByNode(node_type='school', name=nodeName)
	answer = list(searchResult)
	print(answer)
	return HttpResponse(json.dumps(answer,ensure_ascii=False))
