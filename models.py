#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 15:56
# @Author  : djs
# @FileName: models
# @Software: PyCharm

from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __int__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)
