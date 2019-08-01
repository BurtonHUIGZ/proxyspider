from angelspider.utils import Crawl_IP
import re

class ProxyMetaclass(type):
    """
    元类，在FreeProxyGetter类中加入
    __CrawlFunc__和__CrawlFuncCount__
    两个参数，分别表示爬虫函数和爬虫函数数量
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)
            crawl_ip = Crawl_IP(start_url)
            html = crawl_ip.get_page()
            ip_adress = re.compile(
                '<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>'
            )
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_xicidaili(self):
        for page in range(1, 4):
            start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
            crawl_ip = Crawl_IP(start_url)
            html = crawl_ip.get_page()
            ip_adress = re.compile(
                '<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>'
            )
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    # def crawl_daili66(self):
    #     start_url = 'http://www.66ip.cn/{}.html'
    #     urls = [start_url.format(page) for page in range(1, 5)]
    #     for url in urls:
    #         print('Crawling', url)
    #         crawl_ip = Crawl_IP(url)
    #         html = crawl_ip.get_page()
    #         if html:
    #             doc = pq(html)
    #             trs = doc('.containerbox table tr:gt(0)').items()
    #             for tr in trs:
    #                 ip = tr.find('td:nth-child(1)').text()
    #                 port = tr.find('td:nth-child(2)').text()
    #                 yield ':'.join([ip, port])

    def crawl_89ip(self):
        start_url = 'http://www.89ip.cn/index_{}.html'
        urls = [start_url.format(page) for page in range(1, 5)]
        for url in urls:
            print('Crawling', url)
            crawl_ip = Crawl_IP(url)
            html = crawl_ip.get_page()
            ip_adress = re.compile(
                '<td>\s*(.*)\s*</td>\s*<td>\s*(\d+)\s*</td>'
            )
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            print(re_ip_adress)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace('\t\t', '')

    def crawl_xsdaili(self):
        start_url = 'http://www.xsdaili.com/dayProxy/ip/158{}.html'
        urls = [start_url.format(page) for page in range(0, 4)]
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
                yield result.replace('@', '')


