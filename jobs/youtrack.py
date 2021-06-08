#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 15:32
# @Author  : djs
# @FileName: youtrack
# @Software: PyCharm
import asyncio
import aiohttp
import json
import requests
import time
from jobs.getConfig import conf
from logs import logger

# url = conf.get('request', 'url') + '/api/admin/projects?fields=id,name,shortName'
# headers = {
#       'Authorization': conf.get('request', 'Authorization'),
#       'Cookie': conf.get('request', 'Cookie')
#     }
#
# body = requests.get(url=url, headers=headers)
# print(body.text)
# print(len(json.loads(body.text)))

base_url = conf.get('request', 'url')
num = int(conf.get('request', 'num'))


class Yourtrack():

    def __init__(self, Authorization, Cookie, timeout):
        self.Authorization = Authorization
        self.Cookie = Cookie
        self.timeout = timeout
        self.__headers = {
            'Authorization': self.Authorization,
            'Cookie': self.Cookie
        }

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
        try:
            url = base_url + '/api/workItems?$skip=0$top=500&fields=created,duration(presentation,minutes),author(name),creator(name),date,id,text,type,updated'
            print(url)
            body = requests.get(url=url, headers=self.__headers, timeout=int(self.timeout))
            data = json.loads(body.text)
            print(len(data))
            print(data)
            # result = []
            # for item in data:
            #     temp = {}
            #     temp['created'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('created') // 1000))
            #     temp['author'] = item.get('author').get('name')
            #     temp['creator'] = item.get('creator').get('name')
            #     temp['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('date') // 1000))
            #     temp['id'] = item.get('id')
            #     temp['text'] = item.get('text')
            #     temp['type'] = item.get('type')
            #     temp['updated'] = item.get('updated')
            #     result.append(temp)
            # # result = sorted(data, key=lambda x: x['id'], reverse=True)
            # logger.info(result)
        except Exception as e:
            logger.error(e)



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
        url_format = base_url + "/api/admin/projects/17CJY003/issues?fields=id,summary,customFields(id,name,value(fullName,id,minutes,name,presentation,text))&$top=50000"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url_format, headers=self.__headers) as res:
                resp = await res.text()
                data = json.loads(resp)
                # print(len(data))
                logger.info('收到数据条数：{}'.format(len(data)))
                result = []
                for item in data:
                    temp = {}
                    customFields = item['customFields']
                    for obj in customFields:
                        # print(obj)
                        if isinstance(obj['value'], str):
                            temp[obj['name']] = obj['value']
                        elif isinstance(obj['value'], dict):
                            temp[obj['name']] = obj['value']['name'] if obj['value'].get('name') else obj['value'].get(
                                'minutes')
                        elif isinstance(obj['value'], list):
                            temp[obj['name']] = [o['name'] for o in obj['value']]
                    temp['id'] = item['id']
                    temp['summary'] = item['summary']
                    result.append(temp)
                return result



if __name__ == '__main__':
    youtrack = Yourtrack(
        conf.get('request', 'Authorization'),
        conf.get('request', 'Cookie'),
        conf.get('request', 'timeout')
    )
    # youtrack.get_projects()
    # youtrack.get_workItems()
    # youtrack.get_issue_by_project()
    # youtrack.issue_project()
    # loop = asyncio.get_event_loop()
    # task = loop.create_task(youtrack.async_issue_by_project())
    # loop.run_until_complete(task)
    youtrack.get_workItems()
