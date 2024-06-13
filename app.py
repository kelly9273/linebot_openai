from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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
    "推銷員之死 (Death of a Salesman)": {
        "劇作家": "亞瑟·米勒 (Arthur Miller)",
        "年份": 1949
    },
    "櫻桃園 (The Cherry Orchard)": {
        "劇作家": "安東·契訶夫 (Anton Chekhov)",
        "年份": 1904
    },
    "等待戈多 (Waiting for Godot)": {
        "劇作家": "塞繆爾·貝克特 (Samuel Beckett)",
        "年份": 1953
    },
    "玩偶之家 (A Doll's House)": {
        "劇作家": "亨里克·易卜生 (Henrik Ibsen)",
        "年份": 1879
    },
    "女巫緋聞 (The Crucible)": {
        "劇作家": "亞瑟·米勒 (Arthur Miller)",
        "年份": 1953
    },
    "長日將盡夜未央 (Long Day's Journey Into Night)": {
        "劇作家": "尤金·奧尼爾 (Eugene O'Neill)",
        "年份": 1956
    },
    "認真的重要性 (The Importance of Being Earnest)": {
        "劇作家": "奧斯卡·王爾德 (Oscar Wilde)",
        "年份": 1895
    },
    "伊底帕斯王 (Oedipus Rex)": {
        "劇作家": "索福克勒斯 (Sophocles)",
        "年份": -429  # 公元前
    },
    "慾望街車 (A Streetcar Named Desire)": {
        "劇作家": "田納西·威廉斯 (Tennessee Williams)",
        "年份": 1947
    },
    "麥克白 (Macbeth)": {
        "劇作家": "威廉·莎士比亞 (William Shakespeare)",
        "年份": 1606
    },
    "羅密歐與茱麗葉 (Romeo and Juliet)": {
        "劇作家": "威廉·莎士比亞 (William Shakespeare)",
        "年份": 1595
    },
    "一九八四 (Nineteen Eighty-Four)": {
        "劇作家": "喬治·奧威爾 (George Orwell)",
        "年份": 1949
    },
    "雷雨 (Thunderstorm)": {
        "劇作家": "曹禺 (Cao Yu)",
        "年份": 1934
    },
    "北京人 (Peking Man)": {
        "劇作家": "曹禺 (Cao Yu)",
        "年份": 1941
    },
    "俄狄浦斯王 (Oedipus the King)": {
        "劇作家": "索福克勒斯 (Sophocles)",
        "年份": -429  # 公元前
    },
    "第十二夜 (Twelfth Night)": {
        "劇作家": "威廉·莎士比亞 (William Shakespeare)",
        "年份": 1602
    },
    "皆大歡喜 (As You Like It)": {
        "劇作家": "威廉·莎士比亞 (William Shakespeare)",
        "年份": 1599
    }
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
