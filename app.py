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

### another way using config.ini
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
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



# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)



@handler.add(MessageEvent, message=TextMessage)  # default

def get_answer(message_text):
    
    url = "https://chevadymeowbotqna.azurewebsites.net/qnamaker"
# 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'application/json',
                       'Authorization': 'EndpointKey 9b2c32d0-31e2-469b-8ed8-4ad1c93ad90d'
                   }
               )
    data = response.json()
    try: 
        #我們使用免費service可能會超過限制（一秒可以發的request數）
        if "error" in data:
            return data["error"]["message"]
        #這裡我們預設取第一個答案
            msg = data['msgs'][0]['msg']
            return msg
    except Exception:
        return "Error occurs when finding msg"


def handle_message(event):                  # default
    msg = get_answer(event.message.text)
    line_bot_api.reply_message(event.reply_token,
    TextSendMessage(text=msg))
    print("event.reply_token:", event.reply_token)
    print("event.source.user_id:", event.source.user_id)
    print("event.message.text:", event.message.id)
    print("event.source.type:", event.source.type)
    msg = event.message.text # message from user
    uid = event.source.user_id # user id
    #print(msg)
    #print(uid)
    
 

    # 3. 根據使用者的意圖做相對應的回答
    if msg == "aaa": # 當使用者意圖為aaa時
        # 建立一個 button 的 template
        msg = str(msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0

    elif msg == "bbb": # 當使用者意圖為詢bbb時
        msg = str(msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        return 0


    
    #else: # 聽不懂時的回答
    elif msg == "unknown":
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

