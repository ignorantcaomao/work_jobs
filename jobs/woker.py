from queue import Queue, Empty
import threading
import aiohttp
import json
import requests
import time
from jobs.getConfig import conf
from logs import logger
import collections

base_url = conf.get('request', 'url')
num = int(conf.get('request', 'num'))
timeout = int(conf.get('request', 'timeout'))

headers = {
    'Authorization': conf.get('request', 'Authorization'),
    'Cookie': conf.get('request', 'Cookie')
}
THREAD_POOL_SIZE = 5
# 设置允许5个线程同时运行
semaphore = threading.BoundedSemaphore(5)


def get_data(url, datas, se):
    with se:
        with requests.get(url=url, headers=headers, timeout=timeout) as resp:
            data = json.loads(resp.text)
            datas.append(data)
            print('data: ', data)
            logger.info('收到的条数:{}'.format(len(data)))
            return datas


def main():
    threads = []
    result = collections.deque()
    url_format = base_url + '/api/workItems?&fields=created,duration(presentation,minutes),author(name),creator(name),date,id,text,type,updated&$skip={}&$top={}'
    for i in range(4):
        url = url_format.format(i * 1, 1)
        print(url)
        t = threading.Thread(target=get_data, args=(url, result, semaphore))
        threads.append(t)

    for t in threads:
        t.start()
        t.join()

    return result

if __name__ == '__main__':
    t = main()
    print(t)
    print(len(t[0]))
    print(len(t[1]))
    print(len(t[2]))
    print(len(t[3]))

    # s = 'http://space.techstar.com.cn:8081/api/workItems?&fields=created,duration(presentation,minutes),author(name),creator(name),date,id,text,type,updated&$skip=0&$top=50'
    # r = requests.get(url=s, headers=headers)
    # print(len(json.loads(r.text)))