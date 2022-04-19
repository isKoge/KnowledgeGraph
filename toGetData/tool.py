# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-03-19 22:47:17
Message   : tools
'''
from multiprocessing import BufferTooShort
from get_graph_data import get_data,get_webdata
import json
import os
'''
@message  : 获取学校信息
@param        {*} node_list : the list of the scholar
@return       {*} school_node : the node of school
@return       {*} school_link : the relation of school
'''
def schoolData(scholar_list):

    school_link = []
    school_node = []
    school_node_list = []

    for i in scholar_list :
        school_rel = {}
        if i['work_unit'] :
            school_rel['source'] = i['acc_id']
            school_rel['label'] = 'work_for_school'
            school_rel['target'] = i['work_unit']

            school_link.append(school_rel)
            school_node_list.append(i['work_unit'])

    school_node_set = set(school_node_list)
    school_list = [i for i in school_node_set]

    for a in school_list :
        b = {}
        b['name'] = a
        school_node.append(b)

    return school_node, school_link

'''
@message  : 获取两部分的node和link
@param        {*} 
@return       {*}scholar's node, other's node, link
'''
def mergeData():

    # 获取数据，如果存在则加载，不存在则爬取
    if os.path.exists('graph_data.json'):
        res = get_data()
    else:
        get_webdata()
        res = get_data()    

    # 爬取数据存在两部分实体和关系，组合，去除重复的
    nodes = res[0]["nodes"]
    nodes.extend(res[1]["nodes"])
    nodes_unique = remove_thesame(nodes)

    node_scholar = []
    node_other = []

    # 存储对应关系,一个学术成就对应多位作者
    other2acc_id = {}

    for i in nodes_unique:
        beToAdd = i.pop('properties')
        if i['type'] == 'SCHOLAR':
            node_scholar.append(beToAdd)
        else:
            node_other.append(beToAdd)
            nodeName = beToAdd['name']
            nodeId = beToAdd['acc_id']

            if nodeName not in other2acc_id:
                other2acc_id[nodeName] = [i['type']]
            other2acc_id[nodeName].append(nodeId)

    node2 = node_unique(node_other)
    node3, linkData=schoolData(node_scholar)
    nodeData = node_scholar + node2 + node3

    other2acc_id = remove_noneexit(node_scholar,other2acc_id)

    with open("node_data.json", "w", encoding='utf-8') as f:
        json.dump(nodeData, f)
    #   f.write(resp)
    with open("link_data.json", "w", encoding='utf-8') as f:
        json.dump(linkData, f)
    return nodeData, linkData, other2acc_id
    
'''
@message  : 去除不存在节点的关系映射 
@param    : the list of node['id']    {*} n
@param    : the list of link    {*} l
@return   : list    {*}
'''
def remove_noneexit(nodes, other2id):

    id_list = [i['acc_id'] for i in nodes]
    id_unique = list(set(id_list))

    rel_dict = {}
    for k,v in other2id.items():
        acc_list = []
        acc_list.append(v.pop(0))
        while v:
            a = v.pop()
            if a not in id_unique:continue
            acc_list.append(a)
        rel_dict[k] = acc_list
    return rel_dict
'''
@message  : 通过 id 判别是否在节点或关系队列中存在，去除重复多余的 
@param        {*} the_list
@return       {*}
'''
def remove_thesame(the_list):
    
    id_list = []
    label_list = []

    for i in the_list:
        id_list.append(i['id'])
        label_list.append(i['label'])
    
    id_unique = list(set(id_list))

    res_list = []
    ready_list = []

    while id_unique :
        
        node_id = id_unique.pop()

        for one_node in the_list :
            if (one_node['id'] not in ready_list) and ( one_node['id'] == node_id ) :
                    res_list.append(one_node)
                    ready_list.append(node_id)

    return res_list

'''
@message  : to make the same label paper have make just one node 
@param        {*} nodes
@return       {*}
'''
def node_unique(nodes):
    
    label_list = []
    node_list = []
    for i in nodes:
        if i['name'] not in label_list :
                label_list.append(i['name'])
                node_list.append(i)
    return node_list