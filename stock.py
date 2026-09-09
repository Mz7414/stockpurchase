#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import requests
import time
import datetime
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#全域變數
Token = os.environ.get("TOKEN")
User_id = os.environ.get("USER_ID")

user = {
    "Token" : Token,
    "User_id" : User_id,
    "Prefix" : '【申購通知】\n'
}

def discord(e) :
    Discord_Webhook_URL = os.environ.get("DISCORD_WEBHOOK_URL")
    data = {
        "content": e
    }
    response = requests.post(Discord_Webhook_URL, json=data)
    
try :
    from linebot.v3.messaging import MessagingApi, ApiClient, Configuration
    from linebot.v3.messaging.models import TextMessage, PushMessageRequest
except ImportError as e :
    discord(str(e))
    raise

def line(i) :
    config = Configuration(access_token=user['Token'])
    user_id = user['User_id']      
    msg = user['Prefix']+df[dfc[0]][i]+"\n"+df[dfc[1]][i]+"\n"+df[dfc[2]][i]+"\n"+df[dfc[3]][i]+"\n"+df[dfc[4]][i]+"\n"+df[dfc[5]][i]+"\n"+df[dfc[6]][i]+"\n"+df[dfc[7]][i]+"\n"+df[dfc[8]][i]    
    with ApiClient(configuration=config) as api_client :
        messaging_api = MessagingApi(api_client)    
        try :
            message = TextMessage(text=msg)
            push_request = PushMessageRequest(
                to=user_id,
                messages=[message]
            )    
            messaging_api.push_message(push_message_request=push_request)           
        except Exception as e :
            discord(str(e), msg)
            return
            
#執行錯誤時傳送錯誤通知
def line_error(name,e):
    line("<MangaAndNovel>運行出錯\n"+f"{name}錯誤:{e}")
    
url="https://histock.tw/stock/public.aspx"
resp=requests.get(url)
x=pd.read_html(resp.text)
df=x[0]
mask1=df["承銷張數"]>=900
mask2=df["承銷價"]<=300
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


date = str(datetime.date.today())[5:].replace('-','/')
for i in range(len(df)):
    if str(df['申購期間'][i][11:16]) == date or str(df['申購期間'][i][5:10]) == date:
        line(i)
        time.sleep(2)
