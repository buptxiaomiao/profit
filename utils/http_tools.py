# coding: utf-8

import requests
import json
from random import randint
from utils.const import CONST


class Res(object):
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data


class RequestAPI(object):

    @classmethod
    def get_user_agent(cls):
        i = randint(0, len(CONST.user_agent_list) - 1)
        return CONST.user_agent_list[i]

    @classmethod
    def access_data(cls, url, method='GET', params=None, headers=None, token='', timeout=None, access_headers=None,
                    logger=None):

        if url == '':
            raise Exception(u'url is not allowed empty.')
        if method.upper() not in ('GET', 'POST'):
            raise Exception(u'method:%s is not valid.'.format(method))

        _header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,zh-CN;q=0.9',
            'User-Agent': cls.get_user_agent()
        }
        if headers:
            _header.update(headers)
        headers = _header
        if token:
            headers['Access-Token'] = token
        if access_headers:
            headers.update(access_headers)

        if logger:
            logger.info(u'调用API URL： %s, method: %s, params: %s' % (url, method, params))
        else:
            print(u'调用API URL： %s, method: %s, params: %s' % (url, method, params))
        func = getattr(requests, method.lower())
        try:
            response = func(url, params=params, headers=headers, timeout=timeout)
        except Exception as e:
            if logger:
                logger.error(u'请求: %s失败，error msg:%s' % (url, e.message), exc_info=True)
            else:
                print(u'请求: %s失败，error msg:%s' % (url, e.message))
            response = func(url, params=params, headers=headers, timeout=timeout)

        if logger:
            logger.info(u'请求:%s 返回状态: %s, 结果:%s' % (url, response.status_code, response.content))
        else:
            print(u'请求:%s 返回状态: %s, 结果:%s' % (url, response.status_code, response.content))

        data = response.content
        try:
            data = json.loads(response.content)
        except Exception as e:
            if logger:
                logger.error(u'转化数据失败. %s' % e.message, exc_info=True)
            else:
                print(u'转化数据失败. %s' % e.message)

        return Res(status_code=response.status_code, data=data)
