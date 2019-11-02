#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/5 上午9:12
import os, sys
import random
import time
from multiprocessing.pool import Pool
import requests

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from auxiliary.S3Connect import S3Connect
from settings import REDIS_CLIENT, AWS_S3_BUCKET_NAME
from auxiliary.AccessLog import Logger

logger = Logger().logger


# 上传任务函数
def upload2s3(dest_bucket_name, dest_object_name, image_url):
    s3_conn = S3Connect()
    # 判断object 是否已存在
    is_exist = s3_conn.exist_object(dest_bucket_name, dest_object_name)
    if is_exist:
        # 已存在则跳过
        logger.info('object {} already exists'.format(dest_object_name))
    else:
        # 不存在则进行上传
        response = requests.get(url=image_url, timeout=30)  # 获得bytes类型
        if response.status_code == 200:
            src_data = response.content  # bytes
            s3_conn.put_object(dest_bucket_name, dest_object_name, src_data)
        else:
            logger.info('{} 请求该图片地址失败'.format(image_url))


################################ 多进程  ###############################
if __name__ == "__main__":
    t1 = time.time()
    while True:
        udaan_object_length = REDIS_CLIENT.scard('to_be_put_object')
        logger.info('开始上传图片至S3,总计剩余 {} 张图片待上传'.format(str(udaan_object_length)))
        if udaan_object_length != 0:
            po = Pool(3)  # 开启4个进程
            for i in range(3):  # 一次取4张图片上传
                object_info = REDIS_CLIENT.spop('to_be_put_object')
                if object_info:
                    object_infos = object_info.decode().split('&')
                    object_name, image_url = object_infos[0], object_infos[1]
                    po.apply_async(upload2s3, args=(AWS_S3_BUCKET_NAME, object_name, image_url))
                else:
                    continue
            time.sleep(random.random() * 2)
            po.close()
            po.join()
        else:
            logger.info('全部图片上传完成')
            break
    t2 = time.time()
    logger.info('全部图片上传完成,总耗时:{} s'.format(str(t2 - t1)))
