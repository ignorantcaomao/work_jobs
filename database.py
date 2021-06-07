#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 15:50
# @Author  : djs
# @FileName: database
# @Software: PyCharm

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///./test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine
                                         ))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import User
    Base.metadata.create_all(bind=engine)
