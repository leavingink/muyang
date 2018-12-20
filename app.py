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
#會員系統
def GetUserlist():
	userlist = {}
	file = open("users","r")
	while True:
		temp = file.readline().strip().split(",")
		if temp[0] == "" : break
		userlist[temp[0]] = temp[1]
	file.close()
	return userlist

#登入系統
def Login(event, userlist):
	i = 0
	for user in userlist.keys():
		if event.source.user_id == user:
			return i
		i+=1
	return -1
#寫入資料
def Update(userlist):
	file = open("users","w")
	for user in userlist.keys():
		file.write(user + "," + userlist[user])
	file.close()
#關鍵字系統
def KeyWord(event):
	KeyWordDict = {"泓儒":["text","高醫彭于晏"],
					"殘楓落葉":["text","61487"],
					"牧羊":["text","咩~"],
					"愛你":["sticker","11537","52002743"]}
	
	for k in KeyWordDict.keys():
		if event.message.text.find(k) != -1:
			if KeyWordDict[k][0] == "text":
				line_bot_api.reply_message(event.reply_token, TextSendMessage(text = KeyWordDict[k][1]))
			elif KeyWordDict[k][0] == "sticker":
				line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id = KeyWordDict[k][1],
																				sticker_id = KeyWordDict[k][2]))
			return True
	return False
#按鈕版面
def Button(event):
	line_bot_api.reply_message(event.reply_token,
		TemplateSendMessage(
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
	)
#指令系統
def Command(event):
	tempText = event.message.text.split(",")
	if tempText[0] == "發送" and event.source.user_id == "U5322443a06ba30277383a7f5af47d3f8":
		line_bot_api.push_message(tempText[1], TextSendMessage(text = tempText[2]))
		return True
	else:
		return False
#回復函式
def Reply(event, userlist):
	if not Command(event):
		if  not KeyWord(event):
			if event.message.text == "呼叫":
				Button(event)
			else:
				if userlist[event.source.user_id] == "-1":
					line_bot_api.reply_message(event.reply_token,
						TextSendMessage(text = "你知道台灣最稀有、最浪漫的鳥是哪一種鳥嗎?"))
				userlist[event.source.user_id] = "0"
				else:
					if event.message.text == "黑面琵鷺":
						line_bot_api.reply_message(event.reply_token,
							TextSendMessage(text = "你竟然知道答案!!!"))
					else:
						line_bot_api.reply_message(event.reply_token,
							TextSendMessage(text = "答案是：黑面琵鷺!!!因為每年冬天，他們都會到台灣來\"壁咚\""))
					userlist[event.source.user_id] = "-1"
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	try:
		userlist = GetUserlist()
		clientindex = Login(event, userlist)
		if clientindex > -1:
			Reply(event, userlist)
			if event.source.user_id != "U5322443a06ba30277383a7f5af47d3f8":
				line_bot_api.push_message("U5322443a06ba30277383a7f5af47d3f8", TextSendMessage(text = event.source.user_id + "說:"))
				line_bot_api.push_message("U5322443a06ba30277383a7f5af47d3f8", TextSendMessage(text = event.message.text))
		else:
			userlist[event.source.user_id] = "-1";
			line_bot_api.reply_message(event.reply_token,
				TextSendMessage(text = "註冊成功"))
		Update(userlist)
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
		line_bot_api.push_message(event.source.user_id, TextSendMessage(text=event.source.user_id))
	elif command[0] == "董倫弘":
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text="61487"))
	elif command[0] == "陳俊桐":
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text="41269"))
#處理貼圖
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )
import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
