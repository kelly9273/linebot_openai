from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 確保從環境變數中獲取 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise EnvironmentError("LINE_CHANNEL_ACCESS_TOKEN 和 LINE_CHANNEL_SECRET 必須設置。")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

plays_dict = {
    "哈姆雷特 (Hamlet)": {
        "劇作家": "威廉·莎士比亞 (William Shakespeare)",
        "年份": 1600
    },
    "推銷員之死 (Death of a Salesman)": {
        "劇作家": "亞瑟·米勒 (Arthur Miller)",
        "年份": 1949
    },
    "櫻桃園 (The Cherry Orchard)": {
        "劇作家": "安東·契訶夫 (Anton Chekhov)",
        "年份": 1904
    },
    # 其餘劇本略
}

def find_play_info_by_keyword(keyword):
    matching_plays = {}
    keyword_lower = keyword.lower()
    for play, info in plays_dict.items():
        if keyword_lower in play.lower() or keyword_lower in info['劇作家'].lower():
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
    app.run()
