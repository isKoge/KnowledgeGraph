<!--
 * @Author    : KoGe
 * @Date      : 2022-04-05 12:09:23
 * @Message   : 
-->
# 基于知识图谱的学者资源管理系统
> 项目代码仅供参考，项目中包含的数据只可用于学术等非商业用途。
> 
![img](https://github.com/isKoge/KnowledgeGraph/blob/master/README_IMG/g_system.png "System")
## 关于前端样式
>引用
https://github.com/qq547276542/Agriculture_KnowledgeGraph

> 
> AgriKG: An Agricultural Knowledge Graph and Its Applications[C]. DASFAA (3) 2019: 533-537
## toGetData
> 包括爬取学者网的图谱数据
> https://www.scholat.com/home.html?type=8

转为json格式文件可预览或保留，``graph_data.json``便是后续导入的数据，``node_data.json``为节点数据，``link_data.json``为关系数据。
>``get_graph_data``为爬取函数，``py2neo_graph``为导入数据库函数，``tool``包含数据分解处理以便后续使用的函数。
## webGraph
> 使用Django框架，遵从MTV架构，``urls``包含路由分配
### createUser
>用户模块,处理用户注册，登录，权限
### knowledge_graph
>图谱模块，也就是实体关系模块
1. 在``models``存放的即是图数据库的交互语句，有使用到``py2neo``的，也有直接用查询语句的
2. ``kgforms``为各种表单，如各个节点的属性，包括实体和关系
3. ``views``即视图函数，关于图谱数据的全部函数
## 关于neo4j图数据库配置
> 具体参考官方
> https://neo4j.com/docs/operations-manual/current/backup-restore/offline-backup/

### 版本
本次使用的为 Windows系统的 neo4j 4.4.4 版本
### 导出成 dump 文件
```
bin/neo4j-admin dump --database=neo4j --to=/dumps/neo4j/neo4j.dump
```
导出数据库名为neo4j的数据到/dumps/neo4j/neo4j.dump
此次系统数据已经在目录下
### 导入 dump 文件
```
bin/neo4j-admin load --from=/dumps/neo4j/neo4j.dump --database=neo4j --force
```
从/dumps/neo4j/neo4j.dump导入数据库名为neo4j的数据替换原有数据库

请根据自身数据修改路径
## 修改系统配置
- 在``toGetData``的``py2neo_graph``中修改数据库配置图数据库
- 在``webGraph``中的``knowledge_graph``中的``models``进行配置图数据库
###
## 关于Mysql数据库
使用``pymysql``
在``webGraph``的``webGraph``中的``setting``中设置