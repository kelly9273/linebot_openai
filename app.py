from flask import Flask, request, jsonify

app = Flask(__name__)

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

@app.route('/find_play', methods=['GET'])
def find_play():
    keyword = request.args.get('keyword', '').lower()
    matching_plays = {}
    for play, info in plays_dict.items():
        if keyword in play.lower():
            matching_plays[play] = info
    
    if matching_plays:
        return jsonify(matching_plays)
    else:
        return jsonify({"message": "未找到匹配劇本。"})

if __name__ == '__main__':
    app.run(debug=True)
