# -*- coding: utf-8 -*- 
# @Time : 2019/8/26 下午3:59 
# @Site :  
# @File : CityDistribution.py
import os, sys
import csv
import time

import pymongo

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import CSV_FILE_PATH

MONGO_CLIENT = pymongo.MongoClient(
    host='127.0.0.1',
    port=27017,
    username='admin',
    password='123456',
    connect=False
)
LISTING_DB = MONGO_CLIENT['public_udaan']
ORG_COLLECTION = LISTING_DB['orgs_info']



all_location = ORG_COLLECTION.distinct('location')



t1 = time.time()  # 开始时间
with open(CSV_FILE_PATH + '/udaan城市分布.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['location', 'location count'])
    count = 0
    for location in all_location:
        location_count = ORG_COLLECTION.find({"location": location}).count()
        writer.writerow([location, location_count])
        count += 1

t2 = time.time()
print('共统计 {} 件商品信息，共耗时 {} s'.format(str(count), str(t2 - t1)))