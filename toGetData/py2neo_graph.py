# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-03-15 20:33:55
Message   : connect py to neo4j grapth database and make a graph
'''
from tool import mergeData
from tqdm import tqdm
from py2neo import Graph, Node, Relationship, Subgraph, NodeMatcher

'''
@message  : to create the node of the scholar or the school
@param        {*} n the list of node
@return       {*}
'''
def create_node(n, graph):

    tx = graph.begin()
    node_list = []

    for i in tqdm(n):
        if 'home_page' in i.keys():
            n1 = Node('scholar', **i)
        elif 'application' in i.keys():
            n1 = Node('project', **i)
        elif 'paper_source' in i.keys():
            n1 = Node('paper', **i)
        else:
            n1 = Node('school', **i)
        node_list.append(n1)

    subnodes = Subgraph(node_list)
    tx.create(subnodes)
    tx.commit() 

    print('Create the node success !')
'''
@message  : create the relationship between the scholar and the paper or the project
@param        {*} l the list of relationship
@return       {*}
'''
def create_link(ls, oth2id, graph):

    matcher = NodeMatcher(graph)

    # 创建学者与其工作学校的关系
    for i in tqdm(ls):  
        node1 = matcher.match('scholar', acc_id = i['source']).first()
        node2 = matcher.match('school', name = i['target']).first()
        one_link = Relationship(node1, i["label"], node2)
        graph.create(one_link)
    print('Create the relationship of school success !')

    # 创建学者与其学术著作的关系
    for k,v in tqdm(oth2id.items()):
        type = v.pop(0)
        edge_label = f'Author_of_{type}'
        node2 = matcher.match(type, name = k).first()
        while v :
            a = v.pop(0)
            node1 = matcher.match('scholar', acc_id = a).first()
            one_link = Relationship(node1, edge_label, node2)
            graph.create(one_link)
    print('Create the relationship of scholar success !')
    
'''
@message  : to make a graph include create node and link
@param        {*}
@return       {*}
'''
def makeGraph():
    g = Graph("http://localhost:7474", auth=("neo4j","123456"))
    g.delete_all()

    nodeData, linkData, other2id = mergeData()
 
    create_node(nodeData, g)
    create_link(linkData, other2id, g)




