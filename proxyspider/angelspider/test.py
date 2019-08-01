import requests
import asyncio
import aiohttp
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent,FakeUserAgentError
import random
import re
from angelspider.utils import Crawl_IP
from pyquery import PyQuery as pq

start_url = 'http://www.xsdaili.com/dayProxy/ip/158{}.html'
urls = [start_url.format(page) for page in range(0, 3)]
for url in urls:
    print('Crawling', url)
    crawl_ip = Crawl_IP(url)
    html = crawl_ip.get_page()
    ip_adress = re.compile(
        '(\d+\.\d+\.\d+\.\d+):(\d+@?)'
    )
    # \s* 匹配空格，起到换行作用
    re_ip_adress = ip_adress.findall(str(html))
    print(re_ip_adress)
    for adress, port in re_ip_adress:
        result = adress + ':' + port
        print(result.replace('@', ''))
        # yield result.replace('\t\t', '')



