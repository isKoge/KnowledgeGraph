# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-14 15:21:24
Message   : 
'''
from django.shortcuts import render
from knowledge_graph.models import Neo4j
import json

# 链接 Neo4j 
neo_con = Neo4j()
neo_con.connectDB()

# 初始页面
def index(request):  # index页面需要一开始就加载的内容写在这里
	context = {}
	return render(request, 'kg/index.html', context)

def search_relation(request):
	ctx= {'title' : '<h1>暂未找到相应的匹配</h1>'}
	db = neo_con
	if(request.GET):
		
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