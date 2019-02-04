from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, LocationSendMessage
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
    r = '很抱歉，您說什麼'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if '地點' in msg:
        location_message = LocationSendMessage(
            title='my location',
            address='Tokyo',
            latitude=35.65910807942215,
            longitude=139.70372892916203
        )

        line_bot_api.reply_message(
            event.reply_token,
            location_message)
        return

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎?'
    

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()