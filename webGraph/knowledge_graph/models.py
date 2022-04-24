# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-14 15:21:24
Message   : 
'''
from django.db import models
from py2neo import Graph, Node, Relationship

class Neo4j():
	graph = None
	def __init__(self):
		print("create neo4j class ...")

	def connectDB(self):
		self.graph = Graph("http://localhost:7474", auth=("neo4j","123456"))
	
	# 输出整个知识图谱
	def zhishitupu(self):
		answer = self.graph.run("MATCH (n1:scholar)- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		return answer

	# 根据entity的名称返回关系
	def getEntityRelationbyEntity(self,value):
		answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" +str(value)+"\" RETURN rel,entity2").data()
		return answer

	# 通过实体1输出 实体1->关系->实体
	def findRelationByEntity1(self,entity1):
		answer = self.graph.run("MATCH (n1:scholar {name:\"" + entity1 + "\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		if (len(answer)==0):
			answer = self.graph.run("MATCH (n1)- [rel] -> (n2:paper {name:\"" + entity1 + "\"}) RETURN n1, rel, n2" ).data()
			if(len(answer)==0):
				answer = self.graph.run("MATCH (n1)- [rel] -> (n2:project {name:\"" + entity1 + "\"}) RETURN n1, rel, n2" ).data()
		print(answer)
		return answer

	# 通过实体1+关系输出 实体1->关系->实体
	def findOtherEntities(self, entity1, relation):
		answer = self.graph.run("MATCH (n1:scholar {name:\"" + entity1 + "\"})-[rel:" + relation + "]->(n2) RETURN n1,rel,n2" ).data()
		return answer
	
	# 通过实体2+关系输出 实体->关系->实体2
	def findOtherEntity2(self, entity2, relation):
		answer = self.graph.run("MATCH (n1)- [rel:" + relation + "] ->(n2:paper {name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if (len(answer)==0):
			answer = self.graph.run("MATCH (n1)- [rel:" + relation + "] ->(n2:project {name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		return answer

	# 通过实体2输出 实体->关系->实体2
	def findRelationByEntity2(self,entity2):
		answer = self.graph.run("MATCH (n1)- [rel] -> (n2:paper {name:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
		if (len(answer)==0):
			answer = self.graph.run("MATCH (n1)- [rel] -> (n2:project {name:\"" + entity2 + "\"}) RETURN n1,rel,n2" ).data()
		return answer
	
	#根据两个实体查询它们之间的最短路径
	def findRelationByEntities(self,entity1,entity2):
		answer = self.graph.run("MATCH p=(p1:scholar {name:\"" + str(entity1) + "\"})-[*..3]-(p2:scholar{name:\""+str(entity2)+"\"}) RETURN p").to_series()
		# answer = self.graph.run("MATCH (p1:scholar {name:\"" + str(entity1) + "\"}),(p2:scholar{name:\""+str(entity2)+"\"}),p=shortestpath((p1)-[*..10]-(p2)) RETURN p").to_series()
		relationDict = []
		if answer is not None:
			for answer_one in answer:
				for x in answer_one:
					print(x)
					tmp = {}
					start_node = x.start_node
					end_node = x.end_node 
					tmp['n1'] = start_node
					tmp['n2'] = end_node
					tmp['rel'] = x
					relationDict.append(tmp)		
		return relationDict



