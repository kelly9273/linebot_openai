from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging

app = Flask(__name__)

# 替換成你的 Line Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = 'CHANNEL_SECRET'
OPEN_AI_API = 'OPEN_AI_API'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

plays_dict = {
    "哈姆雷特 (Hamlet)": {
        "劇作家": "威廉·莎士比亞 (William Shakespeare)",
        "年份": 1600
    },
    "雷雨 (Thunderstorm)": {
        "劇作家": "曹禺 (Cao Yu)",
        "年份": 1934
    },
    "北京人 (Peking Man)": {
        "劇作家": "曹禺 (Cao Yu)",
        "年份": 1941
    },
}

def find_play_info_by_keyword(keyword):
    matching_plays = {}
    for play, info in plays_dict.items():
        if keyword.lower() in play.lower():
            matching_plays[play] = info
    
    if matching_plays:
        return matching_plays
    else:
        return "此劇本尚未收錄於字典中。"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@app.route("/webhook", methods=['POST'])
def webhook():
    # 驗證請求的內容是否正確
    if request.method == "POST":
        data = request.get_json()
        app.logger.info("Webhook received data: " + str(data))  # 打印請求的數據
        # 可以在此處添加你的處理邏輯
        return "OK", 200
    else:
        app.logger.error("Invalid request method.")
        return "Invalid request method", 400

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    keyword = event.message.text
    matching_plays = find_play_info_by_keyword(keyword)
    
    if isinstance(matching_plays, str):
        response = matching_plays
    else:
        response = "符合關鍵字的劇本：\n"
        for play, info in matching_plays.items():
            response += f"劇本名稱：{play}，劇作家：{info['劇作家']}，年份：{info['年份']}\n"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()
