#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import requests
import time
import datetime

url="https://histock.tw/stock/public.aspx"
resp=requests.get(url)
x=pd.read_html(resp.text)
df=x[0]
mask1=df["承銷張數"]>=1000
mask2=df["承銷價"]<=90
mask3=df["備註"]!="已截止"

df=df[mask1 & mask2 & mask3]
df.rename(columns={"股票代號 名稱":"股票"},inplace=True)
df.reset_index(drop=True,inplace=True)
dfc=df.columns.values.tolist()

for i in range(len(dfc)):
    for j in range(len(df)):
        df[dfc[i]][j]=dfc[i]+"："+str(df[dfc[i]][j])

dfc.pop(4)
dfc.pop(6)
dfc.pop(7)
dfc.pop(8)
dfc.pop(9)

def line(i) :
    url = 'https://notify-api.line.me/api/notify'
    token = 'BlyIANO5jJELyiuTsuhsJMBfRrnsvMz4BvuC7hIBvG3'
    headers = {
    'Authorization': 'Bearer ' + token    # 設定權杖
    }
    data = {
    'message':
        "\n"+
        df[dfc[0]][i]+"\n"+    # 設定要發送的訊息
        df[dfc[1]][i]+"\n"+
        df[dfc[2]][i]+"\n"+
        df[dfc[3]][i]+"\n"+
        df[dfc[4]][i]+"\n"+
        df[dfc[5]][i]+"\n"+
        df[dfc[6]][i]+"\n"+
        df[dfc[7]][i]+"\n"+
        df[dfc[8]][i]
    }
    data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法
date = str(datetime.date.today())[5:].replace('-','/')
for i in range(len(df)):
    if str(df['申購期間'][i][11:16]) == date or str(df['申購期間'][i][5:10]) == date:
        line(i)
        time.sleep(2)

