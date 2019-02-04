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

line_bot_api = LineBotApi('DOUQxyDSFUAvBGADpMTB2Z044fdjhSM+pAoennFYYla54XTPS8nsEyoq1vXGGt6FXecQd5/v4tEhin29Zjd3MSjZTH4hrU4ysUPCTcfSF44KcHlX/nzLYobtDDK9mMhfwPXSyOtnyrF/P+ZwVqQNywdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('664a3d5ee3aa06c9e0f75cf5208592d1')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    s = '你好'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()