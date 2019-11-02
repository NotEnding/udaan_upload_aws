#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/4 上午10:46
import os, sys, time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import LISTING_COLLECTION, REDIS_CLIENT
from auxiliary.AccessLog import Logger

logger = Logger().logger


class DatabaseQuery:

    def query_data(self):
        cursor = LISTING_COLLECTION.find({}, {'listingId': 1, 'orgId': 1, 'listingOrSalesUnitImageAssets': 1})
        return cursor

    def parse_data(self):
        cursor = self.query_data()
        count = 0
        for datas in cursor:
            for images in datas['listingOrSalesUnitImageAssets']:
                images_size = str(images['original']['width']) + '*' + str(images['original']['height'])
                images_name = images_size + '_' + images['original']['uri'][37:].strip('')
                images_uri = images['original']['uri']
                object_name = datas['orgId'] + '/' + datas['listingId'] + '/' + images_name
                # 格式： object_name&image_url ,存入队列
                val = object_name + '&' + images_uri
                REDIS_CLIENT.sadd('to_be_put_object', val)
            count += 1
        return count


if __name__ == "__main__":
    # 初始化 将全部待下载的图片加入到队列
    t1 = time.time()
    logger.info('开始查询全部商品的图片')
    databasequery = DatabaseQuery()
    count = databasequery.parse_data()
    t2 = time.time()
    logger.info('全部待下载图片加入队列成功,共计 {} 商品,共计耗时:{}'.format(str(count), str(t2 - t1)))
