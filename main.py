# python

from bs4 import BeautifulSoup
import requests
import pandas as pd

import datetime
import json

import jsonpath
now = datetime.datetime.now(tz=None)
today_s = now.strftime('%Y%m%d')


url = 'https://www.zhihu.com/billboard'
r = requests.get(url=url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'})
bs = BeautifulSoup(r.text,features="lxml") 


A = bs.select('body')[0]
rk = A.find_all('div',class_='HotList-itemIndex')
title = A.find_all('div',class_='HotList-itemTitle')
hot_d = A.find_all('div',class_='HotList-itemMetrics') 

# 问题地址，在js数据中
res1=jsonpath.jsonpath(json.loads(bs.find('script', id='js-initialData').string),'$..hotList')[0]
url_list = []
for i in range(0,len(res1)):
    url_list.append(res1[i]['target']['link']['url'])
#     extra_list.append(res1[i]['target']['excerptArea']['text'])

df = pd.DataFrame(index = list(range(0,len(rk))), columns = ['rk','content','hot','link'])
df['rk'] = [ i.contents[0] for i in rk]
df['content'] = [ i.contents[0] for i in title]
df['hot'] = [ i.contents[0] for i in hot_d]

df['link'] = url_list

df.to_csv('data/zhihu/zhihuhotlist_'+today_s+'.csv',index=False)
