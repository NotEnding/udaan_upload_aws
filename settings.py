#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/3 下午5:37
##################### aws server 账号信息############################
AWS_REGION_NAME = 'aws region name'
AWS_S3_ACCESS_KEY_ID = "key id"
AWS_S3_SECRET_ACCESS_KEY = "key secret"
AWS_S3_BUCKET_NAME = '存储桶名称'
####################################################################

#################### mongo config ##########################
# import pymongo
#
# MONGO_CLIENT = pymongo.MongoClient(
#     host='127.0.0.1',
#     port=27017,
#     username='admin',
#     password='123456',
#     connect=False
# )
# LISTING_DB = MONGO_CLIENT['public_udaan']
# LISTING_COLLECTION = LISTING_DB['listings_info']
# ORG_COLLECTION = LISTING_DB['orgs_info']

################### redis config  #########################
import redis
# 创建redis连接池
REDIS_CONF = {
    "host": '127.0.0.1',
    "port": 6379,
    "password": 'qwer',
    "db": 1
}
REDIS_POOL = redis.ConnectionPool(**REDIS_CONF)
REDIS_CLIENT = redis.Redis(connection_pool=REDIS_POOL)


################### iamge path ##############################
# ROOT_IMAGE_PATH = '/home/zhengke/Coding/image_file'

################### log path ##############################
LOG_PATH = '/XXX/log'

################### csv file path ########################
CSV_FILE_PATH = '/XXXx/csv_file'

################## clothing 品类名称 #######################
CLOTHING_CATEGORIES = ['clothing_women', 'clothing_men', 'clothing_ethnic', 'clothing_western', 'clothing_kids','clothing_fabric', 'clothing_home_furnishing', 'clothing_innerwear']