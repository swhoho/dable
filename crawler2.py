# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from model import News
from model import Comment
from model import Similarity
server = 'ec2-35-161-71-119.us-west-2.compute.amazonaws.com'
connection_string = 'mysql+mysqldb://root:gozjqkqh1@{}:3306/Test'.format(server)
engine = create_engine(connection_string, pool_recycle = 3600, encoding='utf-8')
Session = sessionmaker(bind=engine)





import requests
from bs4 import BeautifulSoup
from newsdao import NewsDAO
import re
import json


def find_a(tags):
    return tags.name == 'a' and not tags.has_attr('class') and tags.has_attr('href')

class NaverNewsCrawler(object):
    def __init__(self, newsdao, urls):
        self.newsdao = newsdao
        self.urls = urls

    def crawl_link(self):
        for url in self.urls:
            res = requests.get(url)
            content = res.content

            soup = BeautifulSoup(content)

            table = soup.find('table', attrs = {'class' : 'container'})
            for a in table.find_all(find_a):
                link = a['href']
                self.crawl_title_content(link)
                self.crawl_comment(link)

    def crawl_title_content(self, link):
        res = requests.get(link)
        content = res.content

        soup = BeautifulSoup(content)

        title = soup.find('h3', attrs = {'id' : 'articleTitle'}).get_text()
        content = soup.find('div', attrs = {'id' : 'articleBodyContents'}).get_text().strip()
        #print link
        #print str(title)
        #print str(content)

        self.newsdao.save_news(link, str(title), str(content))

    def crawl_comment(self, link):
        headers = {}
        headers['referer'] = link
        oid = re.findall('oid=(\d+)', headers['referer'])
        aid = re.findall('aid=(\d+)', headers['referer'])

        url = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_it&pool=cbox5&lang=ko&country=KR&objectId=news{}%2C{}&categoryId=&pageSize=1000&indexSize=1&groupId=&page=1&sort=FAVORITE'.format(oid[0],aid[0])
        response = requests.get(url, headers = headers)

        m = re.search('_callback\((.*)\)', response.content)
        comments = json.loads(m.group(1))
        ab = len(comments['result']['commentList'])

        session = Session()

        for i in range(ab):
                a = comments['result']['commentList'][i]['contents']
                comment1 = Comment(url = url, comment = str(a))
                try:
                    session.add(comment1)
                    session.commit()
                except:
                    continue

        session.close()



urls = ['http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=10{}'.format(5)]
newsdao = NewsDAO()

crawler = NaverNewsCrawler(newsdao, urls)
crawler.crawl_link()
'newsdao.get_news_by_similarity()'
