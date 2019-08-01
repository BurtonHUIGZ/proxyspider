import redis
from angelspider.error import PoolEmptyError
from angelspider.settings import HOST, PORT, PASSWORD


class RedisClient(object):
    """
    client redis
    """
    def __init__(self, host=HOST, port=PORT, password=PASSWORD):
        if password:
            self._db = redis.Redis(host=host, port=port, password=password)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        从redis中获取proxy
        :param count: 获取数量
        :return:
        """
        proxies = self._db.lrange('proxies', 0, count-1)
        self._db.ltrim('proxies', count, -1)
        return proxies

    def put(self, proxy):
        """
        向redis中从右侧添加代理
        :param proxy:
        :return:
        """
        self._db.rpush('proxies', proxy)

    def pop(self):
        """
        从右边获取代理
        :return:
        """
        try:
            return self._db.rpop('proxies').decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def quene_len(self):
        """
        get length from quene
        :return:
        """
        return self._db.llen('proxies')

    def flush(self):
        """
        清空数据库
        :return:
        """
        self._db.flushall()

# if __name__ == '__main__':
#     conn = RedisClient()
#     conn.put('192.168.1.1')
#     print(conn.get())
