import random
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('njN05CY4QQl1cO04L7oIs+P5QPsfeIJ02Q3fDBWfhjT8dDnpOeG8E7FTew2BnYBfEiCkTTuYvtEfAY+ec6Zn/xjJcdPsPAMy3zHm3N8OgSbpMQjyhlkzQI1pDWwwsOgXf6636IkpdJ0ENpDIYG8G9gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('ec91f3c5fbdb8ddee9637a87fde5098b')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text = Reply(event.message.text))
    line_bot_api.reply_message(event.reply_token, message)

def Reply(text):
    list = ["三民金城武", "高醫彭于晏", "呼吸孔劉"]
    if text.find("Hi")!=-1:
        return "ㄤㄤ"
    elif text.find("泓儒" or "卡巴拉斯" or "Caballas")!=-1:
        return text = random.choice(list)
    else:
        return text
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
