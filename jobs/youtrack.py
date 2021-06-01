#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 15:32
# @Author  : djs
# @FileName: youtrack
# @Software: PyCharm
import json
import requests
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


class Yourtrack():

    def __init__(self, Authorization, Cookie, timeout):
        self.Authorization = Authorization
        self.Cookie = Cookie
        self.timeout = timeout
        self.__headers = {
            'Authorization': self.Authorization,
            'Cookie': self.Cookie
        }

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
            print(e)


if __name__ == '__main__':
    youtrack = Yourtrack(
        conf.get('request', 'Authorization'),
        conf.get('request', 'Cookie'),
        conf.get('request', 'timeout')
    )
    youtrack.get_projects()
