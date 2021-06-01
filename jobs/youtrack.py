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
            url = base_url + '/api/workItems?fields=created,duration(presentation,minutes),author(name),creator(name),date,id'
            body = requests.get(url=url, headers=self.__headers, timeout=int(self.timeout))
            data = json.loads(body.text)
            print(len(data))
            for item in data:
                created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('created') // 1000))
                author = item.get('author').get('name')
                creator = item.get('creator').get('name')

            # result = sorted(data, key=lambda x: x['id'], reverse=True)
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

    async def async_issue_by_project(self):
        try:
            url_format = base_url + "/api/admin/projects/17CJY003/issues?fields=id,summary,customFields(id,name,value(fullName,id,minutes,name,presentation,text))&$skip={}&$top={}"
            result = []
            async with aiohttp.ClientSession() as session:
                index = 0
                while True:
                    print(index)
                    new_url = url_format.format(num * index, num * (index + 1))
                    print(new_url)
                    async with session.get(url=new_url, headers=self.__headers) as res:
                        resp = await res.text()
                        data = json.loads(resp)
                        print(len(data))
                        result += data
                        if len(data) == 0:
                            break
                        else:
                            index += 1
                        # data = json.loads(resp)
                        # for item in data:
                        #     customFields = item.get('customFields')
                        #     print([{k.get('name'): k.get('value').get('name')} for k in customFields])
                            # Type = customFields[0].get('value').get('name')
                            # 优先级 = customFields[1].get('value').get('name')
                            # 状态 = customFields[1].get('value').get('name')

            print(len(result))


        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    youtrack = Yourtrack(
        conf.get('request', 'Authorization'),
        conf.get('request', 'Cookie'),
        conf.get('request', 'timeout')
    )
    # youtrack.get_projects()
    # youtrack.get_workItems()
    youtrack.get_issue_by_project()

    # loop = asyncio.get_event_loop()
    # task = loop.create_task(youtrack.async_issue_by_project())
    # loop.run_until_complete(task)
