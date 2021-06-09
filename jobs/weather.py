#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/9 10:31
# @Author  : djs
# @FileName: weather
# @Software: PyCharm
import time
from queue import Queue, Empty
from threading import Thread

import requests

THREAD_POOL_SIZE = 4
cityids = (
    '101210101', '101010100', '101090201',
    '101020100', '101280101', '101230201'
)


def get_weather(cityid):
    api_url = 'http://www.weather.com.cn/data/sk/' + cityid + '.html'
    results = requests.get(api_url)
    results.encoding = 'utf-8'
    weather_info = results.json()['weatherinfo']

    print("%s (tmp/humi): %s/%s" % (
        weather_info['city'],
        weather_info['temp'],
        weather_info['SD']
    ))


def worker(work_queue):
    while not work_queue.empty():
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        get_weather(item)
        work_queue.task_done()


def main():
    work_queue = Queue()
    for id in cityids:
        work_queue.put(id)
    threads = [
        Thread(target=worker, args=(work_queue,)) for _ in range(THREAD_POOL_SIZE)
    ]
    for t in threads:
        t.start()

    work_queue.join()

    while threads:
        threads.pop().join()


if __name__ == '__main__':
    start = time.time()
    main()
    x = time.time() - start
    print(x)
