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

# 链接 Neo4j 
neo_con = Neo4j()
neo_con.connectDB()

# 初始页面
@login_required
def index(request):  # index页面需要一开始就加载的内容写在这里
	context = {}
	return render(request, 'kg/index.html', context)

@login_required
def search_entity(request):
	ctx = {}
	#根据传入的实体名称搜索出关系
	if(request.GET):
		entity = request.GET['user_text']
		#连接数据库
		db = neo_con
		entityRelation = db.getEntityRelationbyEntity(entity)
		if len(entityRelation) == 0:
			#若数据库中无法找到该实体，则返回数据库中无该实体
			ctx= {'title' : '<h1>暂未找到相应的匹配</h1>'}
			return render(request,'kg/entity.html',{'ctx':json.dumps(ctx,ensure_ascii=False)})
		else:
			#返回查询结果
			#将查询结果按照"关系出现次数"的统计结果进行排序
			# entityRelation = sortDict(entityRelation)

			return render(request,'kg/entity.html',{'entityRelation':json.dumps(entityRelation,ensure_ascii=False)})

	return render(request,"kg/entity.html",{'ctx':ctx})

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