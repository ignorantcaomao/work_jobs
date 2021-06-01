#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 15:41
# @Author  : djs
# @FileName: getConfig
# @Software: PyCharm

import os
from configparser import ConfigParser

conf = ConfigParser()
current_dir = os.path.dirname(__file__)
filename = os.path.join(current_dir, 'config.ini').replace('\\', '/')
conf.read(filename)
