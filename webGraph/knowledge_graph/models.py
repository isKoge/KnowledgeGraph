# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-14 15:21:24
Message   : 
'''
from django.db import models
from py2neo import Graph, Node, Relationship, NodeMatcher, Subgraph, RelationshipMatcher

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
	def findByNode(self, node_type=None, **node_key):
		matcher = NodeMatcher(self.graph)
		if node_type:
			answer = matcher.match(node_type, **node_key)
		else:
			answer = matcher.match(labels=None, **node_key)
		return answer
	
	# 根据两个节点查找关系，可查阅两个学者关系
	def findRelBy2Node(self, n1_key, n2_key, n1_type=None, n2_type=None, **rel_message):
		matcher = RelationshipMatcher(self.graph)
		n1 = self.findByNode(self.graph, a=n1_type, **n1_key).first()
		n2 = self.findByNode(self.graph, a=n2_type, **n2_key).first()
		answer = []
		if ('home_page' in n1) and ('home_page' in n2):
			n1_name = n1.get('name')
			n2_name = n2.get('name')
			# print(n1_name,n2_name)
			searchResult = self.graph.run("MATCH p=(n1:scholar {name:\"" + n1_name + "\"})-[*..2]-(n2:scholar{name:\""+  n2_name +"\"}) RETURN p").data()	
			if searchResult:
				for i in searchResult:
					a = i['p'].relationship
					for r in a:
						temp = {}
						temp['n1'] = r.start_node
						temp['n2'] = r.end_node
						temp['rel'] = {}
						if 'paper_id' in temp['n2']:
							temp['rel']['label'] = 'Author_of_paper'
						elif 'application' in temp['n2']:
							temp['rel']['label'] = 'Author_of_project'
						else:
							temp['rel']['label'] = 'work_for_school'
						answer.append(temp)
			else:
				print("不存在此关系！")
		else:
			temp = {}
			searchResult = matcher.match((n1,n2), r_type=None, **rel_message)
			if searchResult:
				relResult = list(searchResult)[0]
				temp['n1'] = relResult.start_node
				temp['n2'] = relResult.end_node
				temp['rel'] = {}
				temp['rel']['label'] = relResult.get('label')
				answer.append(temp)
			else:
				print("不存在此关系！")
		return answer

	# 创建节点
	def createNode(self, node_type, **node_message):
		n = Node(node_type, **node_message)
		self.graph.create(n)
		print('创建节点成功！')
		return 1

	# 创建关系
	def createRel(self, n1_type, n1_key, n2_type, n2_key, **rel_message):
		matcher = NodeMatcher(self.graph)
		n1 = matcher.match(n1_type, **n1_key).first()
		n2 = matcher.match(n2_type, **n2_key).first()
		label = ''
		if n2_type == 'school':
			label = 'work_for_school'
		else:
			label = f'Author_of_{n2_type}'
		rel_message['label'] = label 
		one_link = Relationship(n1, label, n2, **rel_message)
		self.graph.create(one_link)
		print('创建关系成功！')
		return 1
		
	# 修改节点信息
	def updateNode(self, update_message, node_type=None, **node_key):
		answer = list(self.findByNode(node_type, **node_key))
		for k,v in update_message.items():
			answer[0][k] = v
		sub = Subgraph(answer)
		self.graph.push(sub)
		print('修改节点成功')
		return 1
	
	# 修改关系信息
	def updateRel(self):
		pass

	# 删除节点
	def delNode(self, node_type=None, **node_key):
		answer = self.findByNode(node_type, **node_key)
		if answer:
			self.graph.delete(answer)
			print('删除节点成功！')
			return 1
		else:
			print('删除节点不存在！')
	
	# 删除关系
	def delRel(self, n1_key, n2_key, n1_type, n2_type, **rel_message):
		n1 = self.findByNode(node_type=n1_type, **n1_key)
		n2 = self.findByNode(node_type=n2_type, **n2_key)
		if n1 and n2:
			r1 = self.findRelBy2Node(n1_key, n2_key, **rel_message)
			if len(r1) == 1:
				n1_name = list(n1)[0].get('name')
				n2_name = list(n2)[0].get('name')
				self.graph.run("MATCH (n1) - [rel] - (n2) WHERE n1.name=\"" + n1_name + "\"and n2.name=\"" + n2_name + "\" DELETE rel")
				print("删除关系成功！")
				return 1
			else:
				print("不存在待删除关系！")
		else:
			print("不存在待删除关系的节点！")