from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
    msg=event.message.text
    s="你吃飯了嗎"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()