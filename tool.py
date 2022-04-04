# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-03-19 22:47:17
Message   : tools
'''
from get_graph_data import get_data,get_webdata
import json
import os
'''
@message  : to get a set of scholar's school
@param        {*} node_list : the list of the scholar
@return       {*} school_node : the node of school
@return       {*} school_link : the relation of school
'''
def schoolData(scholar_list, id2label):

    school_link = []
    school_node = []
    school_node_list = []

    for i in scholar_list :
        school_rel = {}
        if i['work_unit'] :
            school_rel['source'] = i['id']
            school_rel['label'] = 'work_for_school'
            school_rel['target'] = i['work_unit']

            school_link.append(school_rel)
            school_node_list.append(i['work_unit'])

    school_node_set = set(school_node_list)
    school_list = [i for i in school_node_set]

    for a in school_list :
        b = {}
        b['id'] = a
        b['label'] = a
        b['type'] = 'school'
        school_node.append(b)

        id2label[a] = a

    return school_node, school_link, id2label

'''
@message  : to get a total list and separate the scholar, the other such as paper or project
@param        {*} 
@return       {*}scholar's node, other's node, link
'''
def mergeData():
    if os.path.exists('graph_data.json'):
        res = get_data()
    else:
        get_webdata()
        res = get_data()    
    nodes = res[0]["nodes"]
    links = res[0]["links"]
    
    nodes.extend(res[1]["nodes"])
    links.extend(res[1]["links"])

    node_scholar = []
    node_other = []
    id2label = {}

    for i in nodes:

        id2label[i['id']] = i['label']
        beToAdd = i.pop('properties')
        i.update(beToAdd)

        if i['type'] == 'SCHOLAR':
            node_scholar.append(i)
        else:
            node_other.append(i)

    node1 = remove_thesame(node_scholar)
    nodeOther = remove_thesame(node_other)
    node2 = node_unique(nodeOther)

    link1 = remove_noneexit(nodes, links, node_other)
    node3, link2, id2label =schoolData(node1, id2label)

    nodeData = node1 + node2 + node3
    linkData = link1 + link2

    with open("node_data.json", "w", encoding='utf-8') as f:
        json.dump(nodeData, f)
    #   f.write(resp)
    with open("link_data.json", "w", encoding='utf-8') as f:
        json.dump(linkData, f)
    with open("id2label_data.json", "w",) as f:
        json.dump(id2label, f)
    return nodeData, linkData, id2label
    
'''
@message  : remove the unexit node in the link and merge the link 
@param    : the list of node['id']    {*} n
@param    : the list of link    {*} l
@return   : list    {*}
'''
def remove_noneexit(nodes, links, node_other):

    node_scholar_id_list = [i['id'] for i in nodes]
    node_other_id_list = [i['id'] for i in node_other]
    node_scholar_id_unique = list(set(node_scholar_id_list))
    node_other_id_unique = list(set(node_other_id_list))

    rel_list = []
    for i in links :
        if i['label'] == 'like':continue
        elif (i['source'] not in node_scholar_id_unique) or (i['target'] not in node_other_id_unique):continue
        rel_list.append(i)
    return rel_list
'''
@message  : remove the same in the list 
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
        if i['label'] not in label_list :
                label_list.append(i['label'])
                node_list.append(i)
    return node_list