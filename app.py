import requests
import re
import configparser
import os
import random
import pandas as pd
import runpy
#叫入並執行其他.py用
import urllib
import time
import tempfile
import apiai
import json
from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from imgurpython import ImgurClient
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

##### Function Import #####

##### Main #####

app = Flask(__name__)

''' ### broke
### hidden in Heroku Config Vars
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
SECRET = os.environ.get('SECRET')
DIALOGFLOW_CLIENT_ACCESS_TOKEN = os.environ.get('DIALOGFLOW_CLIENT_ACCESS_TOKEN')
print(ACCESS_TOKEN)
print(SECRET)
print(GOOGLE_API_KEY)
print(DIALOGFLOW_CLIENT_ACCESS_TOKEN)

ai = apiai.ApiAI(DIALOGFLOW_CLIENT_ACCESS_TOKEN)
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)
'''

### another way using config.ini
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
ai = apiai.ApiAI(config['Dialogflow']['DIALOGFLOW_CLIENT_ACCESS_TOKEN'])



static_tmp_path = os.path.join(os.path.dirname(__file__), 'static')


### this part is constant  don't change
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'

# ================= 語言客製區 Start =================
def is_alphabet(uchar):
    if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
        print('English')
        return "en"
    elif '\u4e00' <= uchar<='\u9fff':
        #print('Chinese')
        print('Chinese')
        return "zh-tw"
    else:
        return "en"
# ================= 語言客製區 End =================



# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)



@handler.add(MessageEvent, message=TextMessage)  # default
def handle_message(event):                  # default
    print("event.reply_token:", event.reply_token)
    print("event.source.user_id:", event.source.user_id)
    print("event.message.text:", event.message.id)
    print("event.source.type:", event.source.type)
    msg = event.message.text # message from user
    uid = event.source.user_id # user id
    #print(msg)
    #print(uid)
    
    # 1. 傳送使用者輸入到 dialogflow 上
    ai_request = ai.text_request()
    #ai_request.lang = "en"
    ai_request.lang = is_alphabet(msg)
    ai_request.session_id = uid
    ai_request.query = msg
    #print(ai_request.lang)
    #print(ai_request.session_id)
    #print(ai_request.query)
    
    # 2. 獲得使用者的意圖
    ai_response = json.loads(ai_request.getresponse().read())
    try:
        user_intent = ai_response['result']['metadata']['intentName']
        print (user_intent)
    except:
        user_intent = "unknown"
        print (user_intent)
    try:
        response = ai_response['result']['fulfillment']['speech']
        print (response)
    except:
        response = "response unknown"
        print (response)        
    
    
    #user_intent = ai_response['result']['metadata']['intentName']
    #print (user_intent)
    #response = ai_response['result']['fulfillment']['speech']
    #print (response)

    # 3. 根據使用者的意圖做相對應的回答
    if user_intent == "WhatToEat": # 當使用者意圖為詢問午餐時
        # 建立一個 button 的 template
        msg = str(response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0

    elif user_intent == "WhatToPlay": # 當使用者意圖為詢問遊戲時
        msg = str(response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0

    ###### TMU Abei 客制區
    
    elif user_intent == "1. enroll-推薦": # 當使用者意圖為 1. enroll-推薦 時
        msg = str(response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0   
    
    elif user_intent == "1. enroll-退選": # 當使用者意圖為 1. enroll-退選 時
        msg = str(response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0    
    
    elif user_intent == "1. enroll-選課": # 當使用者意圖為 1. enroll-選課 時
        msg = str(response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0       
    
    elif user_intent == "1. enroll-選課時間": # 當使用者意圖為 1. enroll-選課時間 時
        msg = str(response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0       
    
    elif user_intent == "2. money-申請": # 當使用者意圖為 2. money-申請 時
        msg = str(response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0 
    
    #else: # 聽不懂時的回答
    elif user_intent == "unknown":
        msg = "挖聽謀ㄟ"
        print (msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0    
    
  


#################### bot群組相關設定 #####################

### 入群問候 (維護中) ###

@handler.add(JoinEvent)
def handle_join(event):
    msg = '大家好~~'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))

if __name__ == '__main__':
    app.run()

