# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-14 15:21:24
Message   : 
'''
from django.db import models
from py2neo import Graph, Node, Relationship, NodeMatcher, Subgraph

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

	# 通过实体1输出 实体1->关系->实体
	def findRelationByEntity1(self,entity1):
		answer = self.graph.run("MATCH (n1:scholar {name:\"" + entity1 + "\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
		if (len(answer)==0):
			answer = self.graph.run("MATCH (n1)- [rel] -> (n2) WHERE n2.name = \"" + entity1 + "\" RETURN n1, rel, n2" ).data()
		return answer

	# 通过实体1+关系输出 实体1->关系->实体
	def findOtherEntities(self, entity1, relation):
		answer = self.graph.run("MATCH (n1:scholar {name:\"" + entity1 + "\"})-[rel:" + relation + "]->(n2) RETURN n1,rel,n2" ).data()
		return answer
	
	# 通过实体2+关系输出 实体->关系->实体2
	def findOtherEntity2(self, entity2, relation):
		answer = self.graph.run("MATCH (n1)- [rel:" + relation + "] -> (n2) WHERE n2.name = \""+entity2+"\" RETURN n1,rel,n2" ).data()
		return answer

	# 通过实体2输出 实体->关系->实体2
	def findRelationByEntity2(self,entity2):
		answer = self.graph.run("MATCH (n1)- [rel] -> (n2) WHERE n2.name = \""+entity2+"\" RETURN n1,rel,n2" ).data()
		return answer
	
	#根据两个实体查询它们之间的最短路径
	def findRelationByEntities(self,entity1,entity2):
		answer = self.graph.run("MATCH p=(p1:scholar {name:\"" + str(entity1) + "\"})-[*..3]-(p2:scholar{name:\""+str(entity2)+"\"}) RETURN p").to_series()
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

	# 根据实体名称输出实体信息
	def findByEntitiy(self,entity):
		answer = self.graph.run("MATCH (n) WHERE n.name = \"" +str(entity)+"\" RETURN n").data()
		return answer

	# 根据作者accid输出实体信息
	def findByaccid(self,accid):
		answer = self.graph.run("MATCH (n) WHERE n.acc_id = \"" +str(accid)+"\" RETURN n").data()
		return answer

	# 根据节点属性寻找节点
	def findByNode(self, node_key, node_type=None):
		matcher = NodeMatcher(self.graph)
		if node_type:
			answer = matcher.match(node_type, **node_key)
		else:
			answer = matcher.match(labels=None, **node_key)
    	

	# 创建节点
	def createNode(self, node_type, node_message):
		n = Node(node_type, **node_message)
		self.graph.create(n)
		return '创建节点成功！'

	# 创建关系
	def createRel(self, n1_type, n1_key, n2_type, n2_key):
		matcher = NodeMatcher(self.graph)
		n1 = matcher.match(n1_type, **n1_key).first()
		n2 = matcher.match(n2_type, **n2_key).first()
		label = ''
		if n2_type == 'school':
			lael = 'work_for_school'
		else:
			label = f'Author_of_{n2_type}'
		rel_message = {'label': label}
		one_link = Relationship(n1, label, n2, **rel_message)
		self.graph.create(one_link)
		return '创建关系成功！'
		
	# 修改节点信息
	def updateNode(self, node_key, update_message, label=None):
		matcher = NodeMatcher(self.graph)
		answer = list(matcher.match(label, **node_key))
		for k,v in update_message.items():
			answer[0][k] = v
		sub = Subgraph(answer)
		self.graph.push(sub)
		return '修改节点成功！'
	
	# 修改关系信息
	def updateRel(self):
		pass

	# 删除节点
	def delNode(self):
		pass
	
	# 删除关系
	def delRel(self):
		pass

