# -*- coding:utf-8 -*-
'''
Author    : KoGe
Date      : 2022-03-18 11:37:37
Message   : 获取 https://res.scholat.com/scholat/scripts/kg/data.gzjs?_dc=5e8ed267fe0 数据
'''

import requests
import json

# 爬取
def get_webdata():
    
    headers = {
     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,v=b3",
     'accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
     'connection': "close",
     'Upgrade-Insecure-Requests': '1',
     'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39",
      }

    page_url = 'https://res.scholat.com/scholat/scripts/kg/data.gzjs?_dc=5e8ed267fe0'
    resp = requests.get(page_url, headers=headers, timeout=20).text[11:-1].rsplit(',',1)[0] + ']'

    with open("graph_data.json", "w", encoding='utf-8') as f:
      # json.dump(resp, f)
      f.write(resp)
      print("载入文件完成...")
    # res_list = json.loads(resp)

# 读取
def get_data():
  with open("graph_data.json", "r", encoding='utf-8') as f:
    res = json.load(f)
  return res

# if __name__=='__main__':
#     # get_webdata()
#     get_data()
    
    
