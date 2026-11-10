
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# 建立中韓翻譯題庫
zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요": "你好",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}

# 建立中日翻譯題庫
zh_jp_dict = {
    "你好": "こんにちは",
    "こんにちは": "你好",
    "謝謝": "ありがとう",
    "ありがとう": "謝謝",
    "對不起": "ごめんなさい",
    "ごめんなさい": "對不起",
    "早安": "おはようございます",
    "おはようございます": "早安",
    "晚安": "おやすみなさい",
    "おやすみなさい": "晚安",
    "老師": "先生",
    "先生": "老師",
    "學生": "学生",
    "学生": "學生",
    "朋友": "友達",
    "友達": "朋友",
    "家人": "家族",
    "家族": "家人",
    "愛": "愛"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/competition')
def competition():
    return render_template('competition.html')


# 中韓、中日翻譯共用路由
@app.route('/ask', methods=['GET', 'POST'])
def ask():

    if request.method == 'POST':

        # 讀取學生輸入的問題
        question = request.form.get('question', '').strip()

        # 讀取選擇的語言
        language = request.form.get('language', 'ko')

        # 根據語言選擇題庫
        if language == 'ko':
            dictionary = zh_ko_dict
            language_name = "韓文"

        elif language == 'jp':
            dictionary = zh_jp_dict
            language_name = "日文"

        else:
            language = 'ko'
            dictionary = zh_ko_dict
            language_name = "韓文"

        # 查詢答案
        answer = dictionary.get(
            question,
            f"抱歉，我目前沒有這個詞的{language_name}對應。"
        )

        # 回傳答案
        return render_template(
            'ask.html',
            question=question,
            answer=answer,
            language=language
        )

    # GET 時給空白欄位
    return render_template(
        'ask.html',
        question="",
        answer="",
        language="ko"
    )


# 課外活動
@app.route('/activities', methods=['GET', 'POST'])
def activities():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()

        answer1 = "抱歉，我目前沒有這個詞的韓文對應。"

        return render_template(
            'activities.html',
            question=question,
            answer=answer1
        )

    return render_template('activities.html', question="", answer="")


# 股票查詢
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()

        if not question:
            answer = "請輸入股票代號，例如 2330。"
        else:
            url = (
                "https://www.twse.com.tw/exchangeReport/"
                f"STOCK_DAY?response=json&stockNo={question}"
            )

            try:
                res = requests.get(url, timeout=10)
                res.raise_for_status()
                data = res.json()

                if data.get("stat") == "OK" and data.get("data"):
                    answer = data["data"][-1][6]
                    answer = f"最近交易日收盤價：{answer} 元"
                else:
                    answer = "查無資料，請確認股票代號或日期。"

            except requests.RequestException:
                answer = "目前無法連接股價查詢服務，請稍後再試。"
            except (ValueError, KeyError, IndexError):
                answer = "資料格式異常，請稍後再試。"

        return render_template(
            'stock.html',
            question=question,
            answer=answer
        )

    return render_template('stock.html', question="", answer="")


@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


@app.route('/club')
def club():
    return render_template('club.html')


@app.route('/electives')
def electives():
    return render_template('electives.html')


@app.route('/ai')
def ai():
    return render_template('ai.html')


@app.route('/pokemon')
def pokemon():
    return render_template('pokemon.html')


# 啟動 Flask
if __name__ == '__main__':
    app.run(debug=True)
