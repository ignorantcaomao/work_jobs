#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 15:32
# @Author  : djs
# @FileName: youtrack
# @Software: PyCharm
import asyncio
from queue import Queue, Empty
from threading import Thread
import aiohttp
import json
import requests
import time
from jobs.getConfig import conf
from logs import logger

base_url = conf.get('request', 'url')
num = int(conf.get('request', 'num'))
timeout = int(conf.get('request', 'timeout'))

headers = {
    'Authorization': conf.get('request', 'Authorization'),
    'Cookie': conf.get('request', 'Cookie')
}
THREAD_POOL_SIZE = 5


def get_data(url):
    with requests.get(url=url, headers=headers, timeout=timeout) as resp:
        data = json.loads(resp.text)
        print(len(data))
        return data


def worker(work_queue):
    while not work_queue.empty():
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        print(item)
        get_data(item)
        work_queue.task_done()


class Yourtrack():

    # 获取所有的项目
    def get_projects(self):
        try:
            url = base_url + '/api/admin/projects?fields=id,name,shortName'
            # url = conf.get('request', 'url') + '/api/admin/projects?customFields?{fields}'
            body = requests.get(url=url, headers=self.__headers, timeout=int(self.timeout))
            data = json.loads(body.text)
            result = sorted(data, key=lambda x: x['id'], reverse=True)
            logger.info(result)
            return result

        except Exception as e:
            logger.error(e)

    def get_workItems(self):
        default_page = 10
        default_num = 1000

        worker_queue = Queue()
        url_format = base_url + '/api/workItems?$skip={}$top={}&fields=created,duration(presentation,minutes),author(name),creator(name),date,id,text,type,updated'

        for i in range(default_page):
            url = url_format.format(i * default_num, default_num)
            worker_queue.put(url)

        threads = [Thread(target=worker, args=(worker_queue, )) for _ in range(THREAD_POOL_SIZE)]

        for t in threads:
            t.start()

        worker_queue.join()

        while worker_queue:
            worker_queue.pop().join()


        # try:
        #     url = base_url + '/api/workItems?$skip=0$top=500&fields=created,duration(presentation,minutes),author(name),creator(name),date,id,text,type,updated'
        #     print(url)
        #     body = requests.get(url=url, headers=self.__headers, timeout=int(self.timeout))
        #     data = json.loads(body.text)
        #     print(len(data))
        #     print(data)
        #     # result = []
        #     # for item in data:
        #     #     temp = {}
        #     #     temp['created'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('created') // 1000))
        #     #     temp['author'] = item.get('author').get('name')
        #     #     temp['creator'] = item.get('creator').get('name')
        #     #     temp['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('date') // 1000))
        #     #     temp['id'] = item.get('id')
        #     #     temp['text'] = item.get('text')
        #     #     temp['type'] = item.get('type')
        #     #     temp['updated'] = item.get('updated')
        #     #     result.append(temp)
        #     # # result = sorted(data, key=lambda x: x['id'], reverse=True)
        #     # logger.info(result)
        # except Exception as e:
        #     logger.error(e)

    def get_issue_by_project(self):
        try:
            url_format = base_url + "/api/admin/projects/17CJY003/issues?fields=id,summary,customFields(id,name,value(fullName,id,minutes,name,presentation,text))&$skip={}&$top={}"
            result = []
            index = 0
            while True:
                new_url = url_format.format(num * index, num * (index + 1))
                print(new_url)
                body = requests.get(url=new_url, headers=self.__headers)
                data = json.loads(body.text)
                print(len(data))
                result += data
                if len(data) == 0:
                    break
                else:
                    index += 1
            print(len(result))
            # url = base_url + "/api/admin/projects/17CJY003/issues?fields=id,summary,customFields(id,name,value(fullName,id,minutes,name,presentation,text))&$skip=0&$top=50"
            # body = requests.get(url=url, headers=self.__headers)
            # data = json.loads(body.text)
            # print(len(data))
            # for item in data:
            #     created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('created')//1000))
            #     author = item.get('author').get('name')
            #     creator = item.get('creator').get('name')

            # result = sorted(data, key=lambda x: x['id'], reverse=True)
            # logger.info(result)
        except Exception as e:
            logger.error(e)

    def issue_project(self):
        url_format = base_url + "/api/admin/projects/17CJY003/issues?fields=id,summary,customFields(id,name,value(fullName,id,minutes,name,presentation,text))&$top=50000"
        print(time.time())
        r = requests.get(url=url_format, headers=self.__headers, stream=True)
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(json.loads(decoded_line))
        print(time.time())

    async def async_issue_by_project(self):
        url_format = base_url + "/api/admin/projects/17CJY003/issues?fields=id,summary,customFields(id,name,value(fullName,id,minutes,name,presentation,text))&$skip={}$top=1000"
        result = []
        async with aiohttp.ClientSession() as session:
            page = 0
            while True:
                new_url = url_format.format(page)
                print(new_url)
                async with session.get(url=new_url, headers=self.__headers) as res:
                    resp = await res.text()
                    data = json.loads(resp)
                    if len(data) == 0:
                        break
                    else:
                        print(len(data))
                        logger.info('收到数据条数：{}'.format(len(data)))

                        for item in data:
                            temp = {}
                            customFields = item['customFields']
                            for obj in customFields:
                                # print(obj)
                                if isinstance(obj['value'], str):
                                    temp[obj['name']] = obj['value']
                                elif isinstance(obj['value'], dict):
                                    temp[obj['name']] = obj['value']['name'] if obj['value'].get('name') else obj[
                                        'value'].get(
                                        'minutes')
                                elif isinstance(obj['value'], list):
                                    temp[obj['name']] = [o['name'] for o in obj['value']]
                            temp['id'] = item['id']
                            temp['summary'] = item['summary']
                            result.append(temp)
                        page += 1
                    return result


if __name__ == '__main__':
    # youtrack = Yourtrack(
    #     conf.get('request', 'Authorization'),
    #     conf.get('request', 'Cookie'),
    #     conf.get('request', 'timeout')
    # )
    # # youtrack.get_projects()
    # # youtrack.get_workItems()
    # # youtrack.get_issue_by_project()
    # # youtrack.issue_project()
    # loop = asyncio.get_event_loop()
    # task = loop.create_task(youtrack.async_issue_by_project())
    # loop.run_until_complete(task)
    # # youtrack.get_workItems()

    youtrack = Yourtrack()
    youtrack.get_workItems()
