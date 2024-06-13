from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import tempfile, os
import openai
import traceback

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
openai.api_key = os.getenv('OPENAI_API_KEY')

def GPT_response(text):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct", 
        prompt=text, 
        temperature=0.5, 
        max_tokens=500
    )
    answer = response['choices'][0]['text'].strip()
    return answer

def translate_text(text):
    prompt = f"請將以下文字翻譯成英文：\n{text}"
    translation = GPT_response(prompt)
    return translation

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    response = ""

    if msg.lower() == "help":
        response = "您可以輸入任何問題來獲取回應。例如：\n1. 翻譯 你好\n2. 問答等"
    elif msg.lower().startswith("翻譯"):
        text_to_translate = msg[3:].strip()
        if text_to_translate:
            try:
                translation = translate_text(text_to_translate)
                response = f"翻譯結果：\n{translation}"
            except:
                app.logger.error(traceback.format_exc())
                response = "翻譯過程中出現錯誤，請稍後再試。"
        else:
            response = "請提供要翻譯的文字，例如：翻譯 你好"
    else:
        try:
            GPT_answer = GPT_response(msg)
            response = GPT_answer
        except:
            app.logger.error(traceback.format_exc())
            response = "處理您的請求時出現錯誤，請稍後再試。"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    response = "您發送了一張圖片，謝謝！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    response = f"您觸發了 postback 事件，數據為：{data}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name} 歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
