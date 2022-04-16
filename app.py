from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage ,LocationSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('Nh+gzoxJwH8c2SMIiIsRG5nXizqqlTranuypfW9R3PDKx9rHJCBEpp7XzJf+kpknT1S4zkudnvL2bKdUyelRuyOlVL/ArRbVuUmzpyWQSxSr6HGZTnKvdlATmsDnz3ofzh2o4441Ct4xXwur4AxQOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b3adeea7da64be952997d2ba8f651b66')


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

#處理接收到的訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg=event.message.text  #使用者輸入訊息
    r="很抱歉，您說了什麼？？"
    if  msg in  ["定位","位置","location"]:
        location_message = LocationSendMessage(
        title='my location',
        address='Tokyo',
        latitude=35.65910807942215,
        longitude=139.70372892916203
        )
        line_bot_api.reply_message(
        event.reply_token,
        location_message)

    if  "貼圖" in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

    if msg in ["hi","Hi","哈囉","你好","你好呀"]:
        r="哈囉"
    elif msg=="你吃飯了嗎":
        r="我還沒吃誒"
    elif msg=="你是誰":
        r="我是shen的line聊天機器人"
    elif "訂位" in msg:
        r="請問您是要訂位嗎？？"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()