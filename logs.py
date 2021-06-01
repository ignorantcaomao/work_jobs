#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 18:02
# @Author  : djs
# @FileName: logs
# @Software: PyCharm

import os
import logging
import logging.handlers

# 创建日志对象
logger = logging.getLogger(__name__)

# 设置logger可输出日志级别范围
logger.setLevel(logging.DEBUG)

# 输出日志到控制台
console_handler = logging.StreamHandler()

# 输出日志到文件中
file_handler = logging.handlers.RotatingFileHandler(
              filename=os.path.dirname(__file__) + '/log.log',
              maxBytes=100,
              backupCount=5)
# file_handler = logging.FileHandler(filename=os.path.dirname(__file__) + '/log.log', mode='a', encoding='UTF-8')
# 添加handler到日志器里
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 设置格式并赋予handler
formatter = logging.Formatter('%(asctime)s - %(filename)s: %(funcName)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# # 输出不同级别日志
# logger.debug("============【开始测试】====================")
# logger.info("============【开始测试】====================")
# logger.warning("============【开始测试】====================")
# logger.critical("============【开始测试】====================")
# logger.error("============【开始测试】====================")


