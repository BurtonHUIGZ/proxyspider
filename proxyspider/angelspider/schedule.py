from angelspider.settings import *
from multiprocessing import Process
from angelspider.db import RedisClient
from asyncio import TimeoutError
import time
from angelspider.error import ResourceDepletionError
from angelspider.getter import FreeProxyGetter
import asyncio
import aiohttp
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError


class ValidityTester(object):
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()

    async def test_singel_proxy(self, proxy):
        """
        测试一个proxy，如果可用，则添加进可用代理池
        :return:
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(self.test_api, proxy=real_proxy, timeout=get_proxy_timeout) as response:
                        if response.status == 200:
                            self._conn.put(proxy)
                            print('Vaild proxy', proxy)
                except (ProxyConnectionError, TimeoutError, ValueError):
                    print('Invaild proxy', proxy)
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as e:
            print(e)
            pass

    def test(self):
        """
        测试所有代理
        :return:
        """
        print('VaildityTester is working')
        try:
            #实例化一个事件循环对象
            loop = asyncio.get_event_loop()
            #协程对象列表
            tasks = [self.test_singel_proxy(proxy) for proxy in self._raw_proxies]
            #将协程对象注册到时间循环对象当中并启动，wait代表阻塞挂起调用接口
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            print('Async Error')


class PoolAdder(object):
    """
    向代理池中添加代理
    """
    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._tester = ValidityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        判断代理池中代理是否充足
        :return:
        """
        if self._conn.quene_len >= self._threshold:
            return True
        else:
            return False

    def add_to_quene(self):
        print('PoolAddr is working')
        proxy_count = 0
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                #将抓取的代理加入检测队列，检测抓取到的代理池
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                #计算检测的代理总数量
                proxy_count += len(raw_proxies)
                #如果代理总数已充足,结束抓取检测
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError




class Schedule(object):

    @staticmethod #静态方法，不能使用类变量和实例变量，是类的工具包,供类调用
    def valid_proxy(cycle=VALID_CHECK_CYCLE):
        """
        get half of proxy from redis
        :param cycle:this tool's running cycle
        :return:None
       """
        #实例化类对象
        conn = RedisClient()
        tester = ValidityTester()

        while True:
            print('Refreshing ip')
            count = int(0.5 * conn.quene_len)
            if count == 0:
                print('Waiting for adding')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    @staticmethod
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD,
                    upper_threshold=POOL_UPPER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE):
        """
        如果代理池中的代理数量小于最小代理数量界限，添加新的代理
        :param lower_threshold:
        :param upper_threshold:
        :param cycle:
        :return:
        """
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if conn.quene_len < lower_threshold:
                adder.add_to_quene()
            time.sleep(cycle)

    def run(self):
        print('Ip processing running')
        validprocess = Process(target=Schedule.valid_proxy)
        check_pool = Process(target=Schedule.check_pool)
        validprocess.start()
        check_pool.start()
