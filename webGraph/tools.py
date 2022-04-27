# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-04-24 23:52:40
Message   : 辅助工具
'''
import re
from knowledge_graph.models import Neo4j


neo_con = Neo4j()
neo_con.connectDB()

# 检查邮箱格式是否合法
def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

# 检查电话格式是否合法
def telephone_check(telephone):
    pattern = re.compile(r'^(13[0-9]|15[0123456789]|18[0-9]|14[57])[0-9]{8}$')
    return re.match(pattern, telephone)

# 检查是否存在节点同 name 在图谱里
def name_check(name):
    db = neo_con
    searchResult = db.findByEntitiy(name)
    if searchResult:
        return len(searchResult)


# 检查是否存在节点同 accid 在图谱里
def accid_check(accid):
    db = neo_con
    searchResult = db.findByaccid(accid)
    if searchResult:
        return len(searchResult)