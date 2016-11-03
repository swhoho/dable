# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import itertools
import datetime
from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from model import News
from model import Comment
from model import Similarity
'from model import Get_cosine'


from sqlalchemy import func,desc


server = 'ec2-35-161-71-119.us-west-2.compute.amazonaws.com'
connection_string = 'mysql+mysqldb://root:gozjqkqh1@{}:3306/Test'.format(server)
engine = create_engine(connection_string, pool_recycle = 3600, encoding='utf-8')
Session = sessionmaker(bind=engine)

class NewsDAO(object):
    def __init__(self):
        pass

    def save_news(self, news_id, title, content):
        session = Session()
        if not self.get_news_by_id(news_id):
            print news_id
            news = News(link = news_id, title = title, content = content, crawl_time = datetime.datetime.now())
            session.add(news)
            session.commit()
        session.close()

    def save_comments(self, url1, comment1):
        session = Session()
        comment = Comment(url = url1, comment = comment1)
        try:
            session.add(comment)
            session.commit()
        except:
            pass

        session.commit()
        session.close()

    def get_news_by_id(self, news_id):
        try:
	    session = Session()
            row = session.query(News).filter(News.link == news_id).first()
            print row
            return row
        except Exception as e:
            print e
        finally:
            session.close()

    def get_news_by_keyword_in_title(self, keyword):
        pass

    def get_news_by_keyword_in_content(self, keyword):
        data = []
        session = Session()
        result = session.query(News).filter(News.content.like('%' + keyword + '%')).all()
        for row in result:
            news = {}
            news['link'] = row.link
            news['title'] = row.title
            news['content'] = row.content

            data.append(news)
        return data

    def get_recent_news(self):
        data = []
        session = Session()
        result = session.query(Comment, News).\
        join(News, News.link == Comment.url).\
        order_by(News.crawl_time).\
        limit(5).\
        all()

        for row in result:
            recent = {}
            recent['title'] = row.News.title
            recent['content'] = row.News.content

            data.append(recent)

        return data

    def get_recent_news2(self):
        data = []
        session = Session()
        result = session.query(Comment, News, func.count(Comment.comment)).\
        join(News, News.link == Comment.url).\
        group_by(Comment.url).\
        order_by(Comment.comment).\
        limit(5).\
        all()
        for row in result:
            recent = {}
            recent['title'] = row.News.title
            recent['content'] = row.News.content
            recent['comment'] = row.Comment.comment
            data.append(recent)

        return data

    def search_comment_page(self):
        data = []
        session = Session()
        result = session.query(Comment, News).\
        join(News, News.link == Comment.url).\
        all()

        for row in result:
            recent = {}
            recent['title'] = row.News.title
            recent['content'] = row.News.content
            recent['comment'] = row.Comment.comment
            data.append(recent)

        return data

    def get_comment_by_keyword(self, keyword, page, page_size):

        data = []
        session = Session()
        result = session.query(Comment).filter(Comment.comment.like('%' + keyword.encode('utf-8') + '%'))\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()

        for row in result:
            recent = {}
            recent['comment'] = row.comment
            data.append(recent)

        return data

    '''
from konlpy.utils import pprint
from konlpy.tag import Kkma
        def get_news_by_similarity(self):
        session = Session()
        result = session.query(News.link, News.content).all()
        data = []
        for row in result:
            news = {}
            news['url'] = row.link
            news['content'] = row.content.decode('utf-8')
            data.append(news)

        kkma = Kkma()
        noun_data = []
        for da in data:
            nouns = {}
            nouns['nouns'] = kkma.nouns(da['content'])
            nouns['url'] = da['url']
            noun_data.append(nouns)
            return data

        final_result = []
        for i in itertools.combinations(noun_data, r = 2):
            data = {}
            ve1 = i[0]['nouns']
            ve2 = i[1]['nouns']
            cosine_d = Get_cosine(ve1, ve2)

            data['similarity'] = cosine_d
            data['first_link'] = i[0]['url']
            data['second_link'] = i[1]['url']
            final_result.append(data)

        from new_model import Similarity

        session = Session()
        for i in final_result:
            cos_sim = Similarity(first_link = i['first_link'], second_link = i['second_link'], Similarity = i['similarity'])
            session.add(cos_sim)

        session.commit()
        session.close()'''

    def get_recommended_news (self, url):
        session = Session()
        data = []
        result = session.query(Similarity.second_link, News.title, News.content)\
        .filter(Similarity.first_link.like('%' + url + '%'))\
        .join(News, News.link == Similarity.second_link)\
        .order_by(desc(Similarity.Similarity))\
        .limit(3)\
        .all()

        for row in result:
            recent = {}
            recent['1. title'] = row.title
            recent['2. recommended_news_content'] = row.content
            recent['3. recommended_news'] = row.second_link

            data.append(recent)

        return data
