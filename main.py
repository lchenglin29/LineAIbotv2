import os
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import requests


GEMINI_API_KEY = "AIzaSyCJ8el9IL-cY5XuAmPyByjZnUxo-rCaALk"

def calling_gemini_api(data):
    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
      print(response.json())
      return response.json()
    else:
      return "Error"

app = Flask(__name__)

help_list = """❗指令列表❗
幫助：取得指令列表
挖礦：挖礦
背包：查看背包
釣魚：釣魚釣魚釣到什麼魚"""

# 這裡需要替換成你的Channel Access Token和Channel Secret
line_bot_api = LineBotApi("ytVm0tpfG8X9kzD5R5wSk/bCXmmpexd3dEqoshh7kokntzR7maDrXZqxl4hm2+5ZKTf5xDJMxVbQzPZQCzkfdjOIB0pgv6CNQEmb3ZlSK9219CvMijKfyXVPWjF7TYWeCfJLDB5oRPvH8FN3fG3YCQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("a55281f160215c491ac18c8c514cfe43")

@app.route("/", methods=['GET'])
def main():
  print("Hello World!")
  return "Hello World!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  user_message = event.message.text
  if user_message == "幫助":
    reply_message = help_list
  else:
    data = {
    "contents": [
        {
            "parts": [{"text": user_message}]
        }
    ]
    }
    reply_message = calling_gemini_api(data)
    if reply_message == "Error":
      reply_message = "發生錯誤，請稍後再試"
    else:
      reply_message = reply_message["candidates"][0]["content"]["parts"][0]["text"]
  line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)