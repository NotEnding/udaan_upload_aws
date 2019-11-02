#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/8 上午9:12
import base64
import urllib
from urllib.parse import urlencode
from urllib.request import urlopen
import os, sys

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import LOG_PATH
from settings import REDIS_CLIENT, LISTING_COLLECTION, ORG_COLLECTION, CLOTHING_CATEGORIES
from auxiliary.AccessLog import Logger


logger = Logger().logger


# 上传百度类
class Imgae2Baidu:

    def __init__(self):
        self.access_token = 'access_token'
        self.same_api = "https://aip.baidubce.com/rest/2.0/realtime_search/same_hq/add"  # 相同图检索入库
        self.similar_api = "https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/add"  # 相似图搜索入库
        self.product_api = "https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/add"  # 商品检索入库
        self.product_search_api = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/search'  # 商品图片-检索

    def get_access_token(self, client_id, client_secret):
        '''
        :https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}
        :param client_id: client_id 为官网获取的API Key
        :param client_secret: client_secret 为官网获取的Secret Key
        :return:
        '''
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'.format(
            client_id=client_id, client_secret=client_secret)
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = eval(response.read().decode())
        if content:
            access_token = content['access_token']
            return access_token
        else:
            return None

    def same2baidu(self, image_url, listingId, id):
        '''
        :https://aip.baidubce.com/rest/2.0/realtime_search/same_hq/add
        :param image_url: 图片url
        :return: 相同图检索-入库
        '''
        f = urlopen(image_url)
        img = base64.b64encode(f.read())
        # 参数
        params = {
            "brief": '{\"name\":\"' + listingId + '\",\"id\":\"' + id + '\"}',
            "image": img,
            "tags": "1,1"
        }
        params = urllib.parse.urlencode(params)
        # 上传至百度
        request_url = self.same_api + "?access_token=" + self.access_token
        request = urllib.request.Request(url=request_url, data=params.encode(encoding='UTF8'))
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urlopen(request)
        content = response.read()
        if content:
            logger.info(content.decode('utf-8'))

    def similar2baidu(self, image_url, listingId, id):
        '''
        :https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/add
        :param image_url: 图片 url
        :return: 相似图搜索入库
        '''
        f = urlopen(image_url)
        img = base64.b64encode(f.read())
        # 参数
        params = {
            "brief": '{\"name\":\"' + listingId + '\",\"id\":\"' + id + '\"}',
            "image": img,
            "tags": "1,1"
        }
        params = urllib.parse.urlencode(params)
        request_url = self.similar_api + "?access_token=" + self.access_token
        request = urllib.request.Request(url=request_url, data=params.encode(encoding='UTF8'))
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urlopen(request)
        content = response.read()
        if content:
            logger.info(content.decode('utf-8'))

    def product2baidu(self, listingId, id, image_url):
        '''
        :https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/add
        :param image_url: 图片url
        :param name : brief listingId 标识
        :param id : brief id 标识,primaryImageAsset id
        :return: 商品检索入库
        '''
        # image 编码
        f = urlopen(image_url)
        img = base64.b64encode(f.read())
        # 参数
        params = {
            "brief": '{\"name\":\"' + listingId + '\",\"id\":\"' + id + '\"}',
            "image": img,
            "tags": "1,1"
        }
        params = urllib.parse.urlencode(params)
        # 上传至百度
        request_url = self.product_api + "?access_token=" + self.access_token
        request = urllib.request.Request(url=request_url, data=params.encode(encoding='UTF8'))
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urlopen(request)
        content = response.read()
        if content:
            content_dict = json.loads(content.decode('utf-8'))  # 转化为字典
            if content_dict.__contains__("error_code"):  # 出错加入到出错队列，后面再处理
                val = listingId + '&' + id + '&' + image_url
                REDIS_CLIENT.sadd('error_task', val)
                logger.error(str(content_dict))
            else:
                logger.info(str(content_dict))

    def product_search(self, image_url):
        '''
        :https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/search
        :param image_url: 商品图片搜索，用于匹配的图片URL
        :return:
        '''
        f = urlopen(image_url)
        img = base64.b64encode(f.read())
        # 参数
        params = {"image": img}
        params = urllib.parse.urlencode(params)
        # 上传至百度
        request_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/search' + "?access_token=" + self.access_token
        request = urllib.request.Request(url=request_url, data=params.encode(encoding='UTF8'))
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urlopen(request)
        content = response.read()
        if content:
            logger.info(content.decode('utf-8'))


if __name__ == "__main__":
    listingId = 'TLTSYE3S0K80YBPCMZF6T8TVBMD9NTY'
    id = 'u/products/tbwqrcjt3e5nn7295lr5.jpg/615/1024'
    image_url = 'https://udaan.azureedge.net/products/tbwqrcjt3e5nn7295lr5.jpg'
    Imgae2Baidu().product2baidu(listingId, id, image_url)
