# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time, Index, DateTime, TIMESTAMP, func, Float
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


server = 'ec2-35-161-71-119.us-west-2.compute.amazonaws.com'
connection_string = 'mysql+mysqldb://root:gozjqkqh1@{}:3306/Test'.format(server)
engine = create_engine(connection_string, pool_recycle = 3600, encoding='utf-8')
Session = sessionmaker(bind=engine)
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
    __table_args__       = (PrimaryKeyConstraint('url', 'comment'), {},)

class Similarity(Base):
    __tablename__ = 'similar'

    first_link            = Column(CHAR(100), nullable = False)
    second_link           = Column(CHAR(100), nullable = False)
    Similarity            = Column(Float, nullable = False)
    __table_args__       = (PrimaryKeyConstraint('first_link', 'second_link'), {},)


Base.metadata.create_all(engine)
