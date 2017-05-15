# coding=utf-8
from flask import Flask
from flask import request
import json
import infoGetter
import config

v2ex_session = {}
header = {}

app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return '<h1>Home</h1>'


@app.route('/newsTitle', methods=['GET'])
def getNews():
    # 获取最近新闻标题
    cate = request.args.get('category')
    dataPath = config.proPath + "dataStorage/"
    if cate == "gongshi":
        dataPath += "news_gongshi.json"
    elif cate == "jianxun":
        dataPath += "news_jianxun.json"
    elif cate == "tongzhi":
        dataPath += "news_tongzhi.json"
    else:
        dataPath += "news_all.json"

    with open(dataPath, "r") as f:
        retData = json.load(f)

    return json.dumps(retData)


@app.route('/newsDetail', methods=['GET'])
def getNewsDetail():
    global v2ex_session
    global header
    # 获取文章ID
    articleId = request.args.get('id')
    # 获取文章信息(利用建立好的session)
    retString = infoGetter.GetDetailFromSystem(v2ex_session, header, articleId)
    # 返回文章内容
    return retString


# @app.route('/signin', methods=['GET'])
# def signin_form():
#     return '''<form action="/signin" method="post">
#               <p><input name="username"></p>
#               <p><input name="password" type="password"></p>
#               <p><button type="submit">Sign In</button></p>
#               </form>'''
#
# @app.route('/signin', methods=['POST'])
# def signin():
#     # 需要从request对象读取表单内容：
#     if request.form['username']=='admin' and request.form['password']=='password':
#         return '<h3>Hello, admin!</h3>'
#     return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    global v2ex_session
    global header

    v2ex_session, header = infoGetter.LoginSystem()

    app.run()
