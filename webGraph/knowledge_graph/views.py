# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-14 15:21:24
Message   : 
'''
from posixpath import split
from django.http import HttpResponse
from django.shortcuts import redirect, render
from knowledge_graph.models import Neo4j
import json
from django.contrib.auth.decorators import login_required
from knowledge_graph.kgforms import *
from django.views.decorators.csrf import csrf_exempt
from tools import remove_none

# 链接 Neo4j 
neo_con = Neo4j()
neo_con.connectDB()

# 初始页面
@login_required
def index(request):  # index页面需要一开始就加载的内容写在这里
	context = {}
	return render(request, 'kg/index.html', context)
	

# 查找实体
def search_entity(request):
	db = neo_con
	searchResult = db.zhishitupu()
	if(request.GET):
		print('--------get---------')
		entity = request.GET['user_text']
		if len(entity) != 0:
			searchResult = db.findRelationByEntity1(entity)
			if(len(searchResult)>0):
				return render(request,'kg/entity.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				print('-----len----0----')
				message = '不存在节点！'
				return render(request,'kg/entity.html',{'message':message})
	return render(request,'kg/entity.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)}) 

@login_required
def search_relation(request):
	ctx = {}
	db = neo_con
	searchResult = db.zhishitupu()
			
	if(request.GET):
		ctx= {'title' : '<h1>暂未找到相应的匹配</h1>'}
		
		entity1 = request.GET['entity1_text']
		relation = request.GET['relation_name_text']
		print(relation)
		entity2 = request.GET['entity2_text']
		searchResult = {}

		#如输入两个学者查看合作节点
		if relation == 'cooperation':
			n1 = {'name':entity1}
			n2 = {'name':entity2}
			searchResult = db.findRelBy2Node(n1,n2,'scholar','scholar')
			if len(searchResult) > 0:
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				return render(request,'kg/relation.html',{'ctx':ctx})

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
			searchResult = db.findShortestPath(entity1,entity2)
			if(len(searchResult)>0):
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				return render(request,'kg/relation.html',{'ctx':ctx})

		#全为空 则输出整个知识图谱
		if(len(entity1)==0 and len(relation)==0 and len(entity2) ==0 ):
			searchResult = db.zhishitupu()
			#print(json.loads(json.dumps(searchResult)))
			return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

		# 若输入entity1,relation,entity2，则按关系输出他们的关系
		if(len(entity1)!=0 and len(entity2)!=0 and len(relation)!=0):
			searchResult = db.findRelByAll(entity1,entity2,relation)
			if(len(searchResult)>0):
				return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})
			elif(len(searchResult)==0):
				return render(request,'kg/relation.html',{'ctx':ctx})
		
	return render(request,'kg/relation.html',{'searchResult':json.dumps(searchResult,ensure_ascii=False)})

@login_required
def NodeManage(request):
	db = neo_con 
	message = {}
	if request.method == 'POST':
		# 选择当前是什么种类，1学者，2论文，3项目
		select_type = (request.get_full_path()).split('/',-1)[-1]
		
		# 选择功能，1增加，2删除，3查找, 4修改
		select_fun = int(request.POST.get('select_fun'))
		print('----------',select_type,'---------',select_fun)
		node_type = ''
		if select_type == 'ScholarManage':
			form = ScholarForm(request.POST)
			node_type = 'scholar'
		elif select_type == 'PaperManage':
			form = PaperNodeForm(request.POST)
			node_type = 'paper'
		elif select_type == 'ProjectManage':
			form = ProjectNodeForm(request.POST)
			node_type = 'project'
		else:
			form = SchoolNodeForm(request.POST)
			node_type = 'school'

		if form.is_valid():
			node_message = form.cleaned_data
			node_name = form.cleaned_data.get('name')
			if select_fun == 1:
				node_message1 = remove_none(node_message)
				if db.findByNode(node_type, **node_message1):
					print(3)
					message = '添加节点失败，节点已经存在，请尝试修改信息后添加！'
					rel = selectForm('n',select_type)
					rel['message'] = message
					return render(request,'kg/NodeManage.html',rel)	
				else:
					print(4)
					db.createNode(node_type, **node_message)
					message = '添加节点成功！'
					rel = selectForm('n',select_type)
					rel['message'] = message
					return render(request,'kg/NodeManage.html',rel)

			elif select_fun == 2:
				node_message = remove_none(node_message)
				answer = db.delNode(node_type, **node_message)
				if answer:
					if answer == 1:
						message = '删除节点成功！'
						rel = selectForm('n',select_type)
						rel['message'] = message
						return render(request,'kg/NodeManage.html',rel)
					else:
						message = '节点存在多个，请选择其中一个！'
						searchResult = list(db.findByNode(node_type, **node_message))
						rel = selectForm('n',select_type)
						rel['message'] = message
						rel['searchResult'] = json.dumps(searchResult,ensure_ascii=False)
						return render(request,'kg/NodeManage.html',rel)
				else:
					message = '删除节点失败，节点不存在！'
					rel = selectForm('n',select_type)
					rel['message'] = message
					return render(request,'kg/NodeManage.html',rel)
			elif select_fun == 3:
				node_message = remove_none(node_message)
				answer = db.findByNode(node_type, **node_message)
				if answer:
					# print(form.cleaned_data)
					searchResult = list(answer)
					rel = selectForm('n',select_type)
					rel['searchResult'] = json.dumps(searchResult,ensure_ascii=False)
					return render(request,'kg/NodeManage.html',rel)
				else:
					message = '不存在节点！'
					rel = selectForm('n',select_type,form=form)
					rel['message'] = message
					return render(request,'kg/NodeManage.html',rel)
			else:
				node_message = remove_none(node_message)
				print(node_message)
				answer = db.updateNode(node_message, node_type, name=node_name)
				if answer:
					if answer == 1:
						message = '修改成功！'
						rel = selectForm('n',select_type,form)
						rel['message'] = message
						return render(request,'kg/NodeManage.html',rel)
					else:
						message = '节点存在多个，请选择其中一个！'
						searchResult = list(db.findByNode(node_type, **node_message))
						rel = selectForm('n',select_type)
						rel['message'] = message
						rel['searchResult'] = json.dumps(searchResult,ensure_ascii=False)
						return render(request,'kg/NodeManage.html',rel)
				else:
					message = '修改失败！'
					rel = selectForm('n',select_type,form)
					rel['message'] = message
					return render(request, 'kg/NodeManage.html', rel)
		else:print(form.errors)
	else:
		print('============else===========')
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
		select_fun = int(request.POST.get('select_fun'))
		# papaerRel: author, accid, name
		# projectRel: participant, accid, name
		# schoolRel: nameScholar, accid. nameSchool
		if form.is_valid():
			# print(form.cleaned_data)
			select_type = form.cleaned_data.get('relType')
			scholarNode = form.cleaned_data.get('ScholarName')
			scholarAccid = form.cleaned_data.get('acc_id')
			toNode = form.cleaned_data.get('nodeName')
			message = form.cleaned_data.get('message')
			# print(select_type)
			if scholarAccid:
				n1_key = {'name':scholarNode,'acc_id':scholarAccid}
			else:
				n1_key = {'name':scholarNode}
			n2_key = {'name':toNode}
		
			if select_fun == 2:
				print(2)
				answer = db.createRel('scholar',n1_key,n2_type=None,n2_key=n2_key,label=select_type,message=message)
				if answer == 1:
					message = '添加关系成功！'
					rel = selectForm('r',select_type)
					rel['message'] = message
					return render(request,'kg/RelManage.html',rel)
				elif answer == 2:
					message = '添加关系失败,节点不存在！'
					rel = selectForm('r',select_type,form)
					rel['message'] = message
					return render(request,'kg/RelManage.html',rel)
				elif answer == 3:
					message = '添加关系失败,学者节点不止一个，请输入学者id！'
					rel = selectForm('r',select_type,form)
					rel['message'] = message
					return render(request,'kg/RelManage.html',rel)
				else:
					message = '添加关系失败！'
					rel = selectForm('r',select_type,form)
					rel['message'] = message
					return render(request,'kg/RelManage.html',rel)

			elif select_fun == 3:
				print(3)
				answer = db.delRel(n1_key,n2_key,'scholar',n2_type=None)
				if answer:
					if answer == 1:
						message = '删除关系成功！'
						rel = selectForm('r',select_type)
						rel['message'] = message
						return render(request,'kg/RelManage.html',rel)
					elif answer == 2:
						message = '同名学者存在多个，请选择其中一个！'
						searchResult = list(db.findByNode(node_type='scholar',**n1_key))
						rel = selectForm('r',select_type)
						rel['message'] = message
						rel['searchResult'] = json.dumps(searchResult,ensure_ascii=False)
						return render(request,'kg/RelManage.html',rel)
					else:
						message = '同名节点存在多个，请选择其中一个！'
						searchResult = list(db.findByNode(node_type=None,**n2_key))
						rel = selectForm('r',select_type)
						rel['message'] = message
						rel['searchResult'] = json.dumps(searchResult,ensure_ascii=False)
						return render(request,'kg/RelManage.html',rel)
				else:
					message = '删除关系失败，关系不存在！'
					return render(request,'kg/RelManage.html',{'form':form, 'message':message})
			else:
				n2_type = select_type.split('_')[-1]
				answer = db.findRelBy2Node(n1_key,n2_key,'scholar',n2_type,label=select_type)
				print(answer)
				if answer:
					searchResult = list(answer)
					rel = selectForm('r',select_type,form)
					rel['message'] = message
					rel['searchResult'] = json.dumps(searchResult,ensure_ascii=False)
					return render(request,'kg/RelManage.html',rel)
				else:
					message = '不存在关系！'
					rel = selectForm('r',select_type,form)
					rel['message'] = message
					return render(request,'kg/RelManage.html',rel)
		else:
			print('----',form.errors)
			message = '不存在节点！'
			rel = selectForm('r','')
			rel['message'] = message
			return render(request,'kg/RelManage.html',rel)
	else:
		form = RelForm()
	return render(request, 'kg/RelManage.html', {'form':form})

# 前端点击返回数据
@csrf_exempt
def jsReturn(request):
	db = neo_con
	nodeName = request.POST.get('data')
	nodeType = request.POST.get('style')
	accid = request.POST.get('accid')
	paperid = request.POST.get('paperid')
	print(nodeName,nodeType,accid)

	if nodeType == '0':
		searchResult = db.findByNode(node_type='scholar', name=nodeName, acc_id=accid)
	elif nodeType == '1':
		searchResult = db.findByNode(node_type='paper', name=nodeName, paper_id=paperid)
	elif nodeType == '2':
		searchResult = db.findByNode(node_type='project', name=nodeName)
	else:
		searchResult = db.findByNode(node_type='school', name=nodeName)
	answer = list(searchResult)
	print(answer)
	return HttpResponse(json.dumps(answer,ensure_ascii=False))

# 关系管理页面Ajax请求
def NodeReturn(request):
	db = neo_con
	nodeName = request.POST.get('data')
	nodeType = request.POST.get('style')
	accid = request.POST.get('accid')
	print(nodeName,nodeType)

	if nodeType == '0':
		searchResult = db.findByNode(node_type='scholar', name=nodeName, acc_id=accid)
	elif nodeType == '1':
		searchResult = db.findByNode(node_type='paper', name=nodeName)
	elif nodeType == '2':
		searchResult = db.findByNode(node_type='project', name=nodeName)
	else:
		searchResult = db.findByNode(node_type='school', name=nodeName)
	answer = list(searchResult)
	print(answer)
	return HttpResponse(json.dumps(answer,ensure_ascii=False))

# 总览
def overview(request):
	db = neo_con
	countByScholar = db.findCountByScholar()
	countBySchool = db.findCountBySchool()
	countByStats = db.findCountStats()
	labels = countByStats['labels']
	tempList = []
	for k,v in labels.items():
		temp = {}
		temp['n.name'] = k
		temp['s'] = v
		tempList.append(temp)
	countByStats['labels'] = tempList
	return render(request,'kg/overview.html',{'countByScholar':json.dumps(countByScholar,ensure_ascii=False),'countBySchool':json.dumps(countBySchool,ensure_ascii=False),'countByStats':json.dumps(countByStats,ensure_ascii=False)})

# 根据类型返回表单
def selectForm(formType, select_type, form=None):
	rel = {
		'formScholar':ScholarForm(),
		'formPaper':PaperNodeForm(),
		'formProject':ProjectNodeForm(),
		'formSchool':SchoolNodeForm(),
		'style':0
	}
	if form:
		if formType == 'n':
			if select_type == 'ScholarManage':
				rel['formScholar'] = form
				rel['style'] = 0
			elif select_type == 'PaperManage':
				rel['formPaper'] = form
				rel['style'] = 1
			elif select_type == 'ProjectManage':
				rel['formProject'] = form
				rel['style'] = 2
			elif select_type == 'SchoolManage':
				rel['formSchool'] = form
				rel['style'] = 3
		elif formType == 'r':
			rel = {}
			rel['form'] = form
	else:
		if formType == 'n':
			if select_type == 'ScholarManage':
				rel['style'] = 0
			elif select_type == 'PaperManage':
				rel['style'] = 1
			elif select_type == 'ProjectManage':
				rel['style'] = 2
			elif select_type == 'SchoolManage':
				rel['style'] = 3
		elif formType == 'r':
			rel = {}
			form = RelForm()
			rel['form'] = form
	return rel