# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time, Index, DateTime, TIMESTAMP, func, Float
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PrimaryKeyConstraint
import re, math
from collections import Counter

Base = declarative_base()

class News(Base):
    __tablename__ = 'naver'

    link            = Column(CHAR(100), primary_key = True, nullable = False)
    title           = Column(TEXT(100), nullable = False)
    content         = Column(TEXT(1000), nullable = False)
    crawl_time      = Column(DateTime, nullable = False)

class Comment(Base):
    __tablename__ = 'comment'

    url           = Column(CHAR(100), nullable = False)
    comment       = Column(CHAR(100), nullable = False)
    __table_args__      = (PrimaryKeyConstraint('url', 'comment'), {},)

class Similarity(Base):
    __tablename__ = 'similar'

    first_link            = Column(CHAR(100), nullable = False)
    second_link           = Column(CHAR(100), nullable = False)
    Similarity            = Column(Float, nullable = False)
    __table_args__       = (PrimaryKeyConstraint('first_link', 'second_link'), {},)



WORD = re.compile(r'\w+')

'''class Get_cosine(ve1, ve2):
    vec1 = Counter(ve1)
    vec2 = Counter(ve2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0

    else:
        return float(numerator) / denominator'''
