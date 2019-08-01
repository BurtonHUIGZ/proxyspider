import requests
import asyncio
import aiohttp
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent,FakeUserAgentError
import random
import re

class Crawl_IP(object):
    """
    获取免费代理页面的html
    """
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN, zh;q=0.8'
    }

    def __init__(self, url, options={}):
        self.url = url
        self.options = options
        self.headers = dict(self.base_headers, **options)

    def get_page(self):
        print('Getting url:', self.url)
        try:
            resp = requests.get(self.url, headers=self.headers)
            print('Getting result', self.url, resp.status_code)
            if resp.status_code == 200:
                return resp.text
        except ConnectionError:
            print('Crawl failed', self.url)
            return None
