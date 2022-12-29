from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, 
                            ConfirmTemplate, MessageAction, FlexSendMessage, QuickReply, QuickReplyButton)
import re
import myfun

import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('channel_access_token')
secret = os.getenv('channel_secret')

app = Flask(__name__)

line_bot_api = LineBotApi(token)
handler = WebhookHandler(secret)

@app.route("/callback", methods=['POST'])
def callback():

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_text = event.message.text

    # 考選部網站最新消息
    if re.match('@最新消息', msg_text):
        try:
            obj = FlexSendMessage(alt_text = '最新消息',contents = myfun.moex_news())
        except:
            obj = TextSendMessage(text = f'error {msg_text}')
    
    # 考選部網站最新考試公告
    elif re.match('@考試公告', msg_text):
        try:
            obj = FlexSendMessage(alt_text = '考試公告',contents = myfun.wfrm_news())
        except:
            obj = TextSendMessage(text = f'error {msg_text}')
    
    # App功能介紹
    elif re.match('@使用說明', msg_text):
        obj =TextSendMessage(myfun.app_introduction())

    # 國考介紹
    elif re.match('@國考介紹', msg_text):
        obj =FlexSendMessage(alt_text = '國考介紹',contents = myfun.test_introduction())   
    # 國考介紹快速回復選單
    elif re.match('@國考類型', msg_text):
        obj = TextSendMessage(text='請點擊', quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label='高普初考', text='@高普初考介紹')),
                QuickReplyButton(action=MessageAction(label='特種考試', text='@特種考試介紹')),
                QuickReplyButton(action=MessageAction(label='國營事業', text='@國營事業介紹'))]))
    elif re.match('@高普初考介紹', msg_text):
        obj =FlexSendMessage(alt_text = '高普初考介紹',contents = myfun.test_introduction_1())
    elif re.match('#高考詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '高考詳細介紹',contents = myfun.test_introduction_1h())
    elif re.match('#普考詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '普考詳細介紹',contents = myfun.test_introduction_1m())
    elif re.match('#初考詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '初考詳細介紹',contents = myfun.test_introduction_1l())
    elif re.match('@特種考試介紹', msg_text):
        obj =FlexSendMessage(alt_text = '特種考試介紹',contents = myfun.test_introduction_2())
    elif re.match('#聯招詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '聯招詳細介紹',contents = myfun.test_introduction_3_1())
    elif re.match('#獨招詳細介紹', msg_text):
        obj =FlexSendMessage(alt_text = '獨招詳細介紹',contents = myfun.test_introduction_3_2())
    elif re.match('@國營事業介紹', msg_text):
        obj =FlexSendMessage(alt_text = '國營事業介紹',contents = myfun.test_introduction_3())

    # 高普考錄取率
    elif re.match('@錄取率排行', msg_text):
        obj = TemplateSendMessage(alt_text='請選擇',
            template=ConfirmTemplate(text='考試類型',
                actions=[MessageAction(label='高考錄取率',text='@高考錄取率'),
                         MessageAction(label='普考錄取率',text='@普考錄取率')]))
    elif re.match('@高考錄取率', msg_text):
        obj =FlexSendMessage(alt_text = '高考錄取率',contents = myfun.acceptance_rate('高考錄取率'))
    elif re.match('@普考錄取率', msg_text):
        obj =FlexSendMessage(alt_text = '普考錄取率',contents = myfun.acceptance_rate('普考錄取率'))

    # 高普考代碼查詢第一層
    elif re.match('@代碼查詢', msg_text):
        obj = TextSendMessage(text='請點擊', quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label='高考', text='@高考代碼')),
                QuickReplyButton(action=MessageAction(label='普考', text='@普考代碼'))]))
    elif re.match('@高考代碼', msg_text):
        obj1 =FlexSendMessage(alt_text = '高考代碼',contents = myfun.subject_id('高考'))
        obj2 = TextSendMessage(text = '請輸入代碼：')
        obj = [obj1, obj2]
    elif re.match('@普考代碼', msg_text):
        obj1 =FlexSendMessage(alt_text = '普考代碼',contents = myfun.subject_id('普考'))
        obj2 = TextSendMessage(text = '請輸入代碼：')
        obj = [obj1, obj2]

    # 高普考代碼查詢第二層
    elif re.match('H', msg_text[0]):
        try:
            obj =FlexSendMessage(alt_text = '高考介紹',contents = myfun.test_subject_introduction('高考', msg_text[1:4]))
        except:
            obj = TextSendMessage(text = f'error {msg_text}')
    elif re.match('S', msg_text[0]):
        try:
            obj =FlexSendMessage(alt_text = '普考介紹',contents = myfun.test_subject_introduction('普考', msg_text[1:3]))
        except:
            obj = TextSendMessage(text = f'error {msg_text}')    
    
    # 高普考考古題連結
    elif re.match('@exam', msg_text[0:5]):
        try:
            obj =FlexSendMessage(alt_text = '考古題', contents = myfun.exam(msg_text[6:]))
        except:
            obj = TextSendMessage(text = f'error {msg_text}')
    elif re.match('#exam', msg_text[0:5]):
        try:
            obj =TextSendMessage(text = myfun.exam_link(msg_text[6:]))
        except:
            obj = TextSendMessage(text = f'error {msg_text}')
    else:
        obj = TextSendMessage(text = f'error {msg_text}')
    line_bot_api.reply_message(event.reply_token, obj)

if __name__ == "__main__":
    app.run(host="192.168.0.107",ssl_context=('LineBot.crt', 'LineBot.key'), port = 443)