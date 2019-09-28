import requests
import json
from flask import Flask


def get_valutes_list():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = json.loads(response.text)
    valutes = list(data['Valute'].values())
    return valutes


app = Flask(__name__)


def create_html(valutes):
    text = '''
<style>
body{
    margin: 0px 0px 0px 0px;
    background: #9f9f9f;
    color: #121212;
    font-family: Tahoma;
    font-size: 12px;
}
table.mTbl{
    border-width: 0px;
    border-style: none;
    padding: 2px;
    width: 100%;
    background: #ffffff;
}
table.mTbl th{
    font-weight: bold:
    text-align: center;
    vertical-align: center;
    background: #9999cc;
    color: #ffffff;
}
table.mTbl tr#csl{
    background: #cc99cc;
}
table.mTbl tr#alt{
    background: #99cc99;
}
</style>
    '''
    style = 'csl'
    text += '<table class="mTbl"><tr><th colspan="$colCount$">Курс валют</th></tr>'
    text += '<tr>'
    cnt = 0
    # --{{ av: следующий блок непонятно какие цели преследует
    for _ in valutes[0]:
        text += f'<th></th>'
        cnt += 1
    # --}}
    text += '<th></th></tr>'
    for valute in valutes:
        text += f'<tr id="{style}">'
        style = 'alt' if 'csl' == style else 'csl'
        for v in valute.values():
            text += f'<td>{v}</td>'
        trend = '^' if float(valute['Value']) > float(valute['Previous']) else (
            'v' if float(valute['Value']) < float(valute["Previous"]) else '='
        )
        text += f'<td align="center">{trend}</td>'
        text += '</tr>'

    text += '</table>'
    text = text.replace('$colCount$', str(cnt + 1))
    return text


@app.route("/")
def index():
    valutes = get_valutes_list()
    html = create_html(valutes)
    return html


if __name__ == "__main__":
    app.run()
