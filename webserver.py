# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from model import News
from model import Comment
from flask import Flask, jsonify,request
from newsdao import NewsDAO
from memcache import MemCache
import uuid
import redis


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hi, Dable!'

@app.route('/test')
def hello_json():
    data = {'name' : 'Hojung', 'family' : 'Yeo'}
    return jsonify(data)

@app.route('/news/search/<keyword>')
def search_news(keyword):

    newsdao = NewsDAO()
    memcache = MemCache()

    id = request.args.get('id')
    apikey = request.args.get('apikey')

    r = redis.Redis(host = 'ec2-35-161-71-119.us-west-2.compute.amazonaws.com', port = 6379)

    if memcache.auth_user(id, apikey):
        data = newsdao.get_news_by_keyword_in_content(str(keyword))

    else:
        data = {'result' : '인증 취소 /auth'}

    return jsonify(data)


@app.route('/auth')
def auth():
    memcache = MemCache()

    id = str(request.args.get('id'))
    apikey = str(uuid.uuid4())

    memcache.hold_user_key(id, apikey)
    return jsonify({'apikey' : apikey})

@app.route('/news/recent')
def search_recent_news():
    newsdao = NewsDAO()
    data = newsdao.get_recent_news()
    return jsonify(data)


@app.route('/comment/search/<keyword>')
def search_comment(keyword):
    newsdao = NewsDAO()
    print type(keyword)
    page = int(request.args.get('page'))
    page_size = int(request.args.get('page_size'))

    data = newsdao.get_comment_by_keyword(str(keyword), page, page_size)
    return jsonify(data)

@app.route('/news/rec')
def recommended_news():
    newsdao = NewsDAO()

    url = request.args.get('url')
    data = newsdao.get_recommended_news(url)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
