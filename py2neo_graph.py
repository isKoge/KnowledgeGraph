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
        n1 = Node(i['type'], **i)
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
def create_link(ls, id2label, graph):

    matcher = NodeMatcher(graph)

    for i in tqdm(ls):
            
        matcher = NodeMatcher(graph)
        node1 = matcher.match("SCHOLAR", id = i['source']).first()

        label_name = i['label'].split('_')[-1].lower()

        targetLabel = id2label[i['target']]
        node2 = matcher.match(label_name, label = targetLabel).first()

        one_link = Relationship(node1, i["label"], node2)

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

    nodeData, relationData, m = mergeData()
 
    create_node(nodeData, g)
    create_link(relationData, m, g)




