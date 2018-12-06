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
#關鍵字
def KeyWord(text):
	KeyWordDict = {"泓儒":"高醫彭于晏","殘楓落葉":"61487","牧羊":"咩~"}
	for k in KeyWordDict.keys():
		if text.find(k) != -1:
			return [True, KeyWordDict[k]]
		return [False]

def Reply(event):
	Ktemp = KeyWord(event.message.text)
	if Ktemp[0]:
		line_bot_api.reply_message(event.reply_token, 
			TextSendMessage(text = Ktemp[1]))
	else:
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text = event.message.text))
def Button(event):
	message = TemplateSendMessage(
		alt_text='yeeeee',
		template=ButtonsTemplate(
			thumbnail_image_url='sheep.png',
			title='題目',
			text='測試',
			actions=[
				PostbackTemplateAction(
					label='TEST',
					text='TEST!!!',
					data='action=buy&itemid=1'
				),
				MessageTemplateAction(
					label='殘楓落葉',
					text='61487'
				),
				URITemplateAction(
					label='Youtube',
					uri='https://www.youtube.com/?hl=zh-CN'
				)
			]
		)
	)
line_bot_api.reply_message(event.reply_token, message)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	try:
		Button(event)
		#Reply(event)
	except Exception as e:
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text=str(e)))
import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
