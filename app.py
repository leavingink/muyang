from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import *
import requests

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
#設定帳號class
class user:
	def _init_(self,ID,Name,Situation):
		self.Nmae = Name
		self.ID = ID
		self.Situation = Situation
#新增一個新使用者
def Signup(user_id,name):
	url = "https://script.google.com/macros/s/AKfycbxn7Slc2_sKHTc6uEy3zmm3Bh_4duiGCXLavUM3RB0a3yzjAxc/exec"
	payload = {
		'sheetUrl':"https://docs.google.com/spreadsheets/d/1_YY_Fh0DTULkXeGnN881DjeVsOZOgRFOqPuGgwnGpfg/edit?usp=sharing",
		'sheetTag':"Sheet1",
		'data':user_id+','+',-1'
	}
	requests.get(url, params=payload)
#取得所有會員資料
def GetUserlist():
	url = "https://script.google.com/macros/s/AKfycbwVs2Si91yKz6m3utpaPtsttbh_lUQ8LOQM3Zud2hPFxXCgW3u1/exec"
	payload = {
		'sheetUrl':"https://docs.google.com/spreadsheets/d/1_YY_Fh0DTULkXeGnN881DjeVsOZOgRFOqPuGgwnGpfg/edit?usp=sharing",
		'sheetTag':"Sheet1",
		'row': 1,
		'col': 1,
		'endRow': 51,
		'enCol': 20
	}
	resp = requests.get(url, params = payload)
	temp = resp.text.split(',')
	userlist = []
	i = 0
	while i < len(temp):
		if temp[i] != "":
			userlist.append(user(temp[i],temp[i+1],temp[i+2]))
			i += 3
		else:
			break
	return userlist
#取得目前使用者的index
def Login(user_id,userlist):
	for user in userlist:
		if user.ID == user_id:
			return userlist.index(user)
	return -1
#寫入資料
def Write(Row,data,Col):
	url = "https://script.google.com/macros/s/AKfycbyBbQ1lsq4GSoKE0yiU5d6x0z2EseeBNZVTewWlSZhQ6EVrizo/exec"
	payload{
		'sheetUrl':"https://docs.google.com/spreadsheets/d/1_YY_Fh0DTULkXeGnN881DjeVsOZOgRFOqPuGgwnGpfg/edit?usp=sharing",
		'sheetTag':"Sheet1",
		'data':data,
		'x':str(Row+1),
		'y':str(Col+1)
	}
	requests.get(url, params = payload)
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
	if event.message.text == "呼叫":
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
	if userlist[clientindex].Situation == '-1':
		if not Command(event):
			if  not KeyWord(event):
				if not Button(event):
					line_bot_api.reply_message(event.reply_token,
						TextSendMessage(text = "你知道台灣最稀有、最浪漫的鳥是哪一種鳥嗎?"))
					Write(clientindex,'0',3)
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
