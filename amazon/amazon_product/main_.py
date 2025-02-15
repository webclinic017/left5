# -*- coding: utf-8 -*-
__author__ = 'xtwxfxk'

import logging, logging.config, time, traceback
from shove import Shove
from concurrent.futures import ThreadPoolExecutor

from spider.best_sell import BestSell, ThreadSet
from spider.base.models import URL_TYPE

import config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('verbose')

multiple = 4

string_proxies = [
    # 'socks4://192.168.1.188:1080',
    # 'socks4://192.168.1.188:1081',
    # 'socks4://192.168.1.188:1082',
    # # 'socks4://192.168.1.188:1083',
    # 'socks4://192.168.1.188:1084',
    '', '', '', ''
]


executor = ThreadPoolExecutor(max_workers=len(string_proxies)*multiple)

url_info = Shove(config.URL_URL_INFO)
key_set = ThreadSet()

key_set = key_set.union(url_info.keys())

bs = []
for i in range(multiple):
    for string_proxy in string_proxies:
        bs.append(BestSell(key_set, string_proxy=string_proxy, url_info_root=config.URL_URL_INFO))


def spider():

    while 1:
        i = 0
        for key, value in url_info.items():
            if not value[3]:
                if value[1] == URL_TYPE.BEST_SELL_CATEGORY:
                   executor.submit(bs[i%len(bs)].categories, url_obj=value)
                if value[1] == URL_TYPE.BEST_SELL_CATEGORY_NEXT:
                   executor.submit(bs[i%len(bs)].category_next, url_obj=value)
                elif value[1] == URL_TYPE.PRODUCT_URL:
                    executor.submit(bs[i%len(bs)].product, url_obj=value)

                i += 1

        logger.info('Wait 5 Second...')
        time.sleep(5)


if __name__ == '__main__':
    spider()







