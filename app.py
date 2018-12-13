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
def KeyWord(event):
	KeyWordDict = {"泓儒":"高醫彭于晏","殘楓落葉":"61487","牧羊":"咩~","取得ID":event.source.user_id}
	for k in KeyWordDict.keys():
		if event.message.text.find(k) != -1:
			return [True, KeyWordDict[k]]
	return [False]
#按鈕版面
def Button(event):
	return TemplateSendMessage(
		alt_text='yeeee',
		template=ButtonsTemplate(
			thumbnail_image_url='https://github.com/leavingink/muyang/blob/master/sheep.png?raw=true',
			title='Eternal',
			text='呼叫',
			actions=[
				PostbackTemplateAction(
					label='陳俊桐',
					data='陳俊桐'
				),
				PostbackTemplateAction(
					label='董倫弘',
					data='董倫弘'
				),
				PostbackTemplateAction(
					label='蔡育霖',
					data='蔡育霖'
				)
			]
		)
	)
#回復函式
def Reply(event):
	tempText = event.message.text.split(",")
	if tempText[0] == "發送" and event.source.user_id == "U391682f77f3c4ed336be50e7f4f9e9f0":
		line_bot_api.push_message(tempText[1], TextSendMessage(text = tempText[2]))
	if tempTxt
	Ktemp = KeyWord(event)
	if Ktemp[0]:
		line_bot_api.reply_message(event.reply_token, 
			TextSendMessage(text = Ktemp[1]))
	elif event.message.text == "呼叫":
		line_bot_api.reply_message(event.reply_token,
			Button(event))
	#else:
		#line_bot_api.reply_message(event.reply_token,
			#TextMessage(text = event.message.text))
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	try:
		Reply(event)
		line_bot_api.push_message("U391682f77f3c4ed336be50e7f4f9e9f0", TextSendMessage(text = event.source.user_id))
		line_bot_api.push_message("U391682f77f3c4ed336be50e7f4f9e9f0", TextSendMessage(text = event.message.text))
	except Exception as e:
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text=str(e)))
#處理PostBack
@handler.add(PostbackEvent)
def handle_postback(event):
	command = event.postback.data.split(',')
	if command[0] == "蔡育霖":
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text="002788"))
		line_bot_api.push_message(event.source.user_id, TextSendMessage(text="汁妹王"))
	elif command[0] == "董倫弘":
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text="61487"))
	elif command[0] == "陳俊桐":
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text="41269"))
import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
