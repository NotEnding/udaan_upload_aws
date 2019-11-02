#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/4 下午2:43
import os, sys
import csv
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import LISTING_DB, CSV_FILE_PATH

listing_collection = LISTING_DB['listings_info']  # 商品表
org_collection = LISTING_DB['orgs_info']  # 店铺表

'''
卖家id	卖家名称	卖家注册时间	location	卖家产品数
'''

t1 = time.time()
org_cursor = org_collection.find({},
                                 {'orgId': 1, 'displayName': 1, 'yearInception': 1, 'location': 1, 'locationCity': 1,
                                  'locationState': 1, 'locationPincode': 1, 'preferredContactNumber': 1})
print('开始获取udaan卖家详情分析')
with open(CSV_FILE_PATH + '/udann卖家信息分析.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ['orgId', 'displayName', 'yearInception', 'location', 'locationCity', 'locationState', 'locationPincode',
         'preferredContactNumber', 'listings'])
    count = 0
    for org_info in org_cursor:
        orgId = org_info['orgId']
        print("正在统计店铺 {} 信息".format(orgId))
        listing_count = listing_collection.find({"orgId": orgId}).count()
        writer.writerow([
            org_info['orgId'], org_info['displayName'], org_info['yearInception'], org_info['location'],
            org_info['locationCity'], org_info['locationState'], org_info['locationPincode'],
            org_info['preferredContactNumber'],
            listing_count
        ])
        count += 1
t2 = time.time()
print('共统计 {} 家店铺信息,共耗时 {} s'.format(str(count), str(t2 - t1)))
