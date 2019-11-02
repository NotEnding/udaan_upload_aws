# -*- coding: utf-8 -*- 
# @Time : 2019/8/17 上午9:56 
# @Site :  
# @File : MoqAnalysis.py
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
供应商id  供应商名称  
'''

t1 = time.time()  # 开始时间
listing_cursors = listing_collection.find({}, {"orgId": 1, "listingMoq": 1, "inferredMoq": 1})  # 商品

with open(CSV_FILE_PATH + '/udaan Moq 分析.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['供应商id', 'listingMoq', 'inferredMoq'])
    count = 0
    for listing_info in listing_cursors:
        # print(type(listing_info['listingMoq']))
        if listing_info['listingMoq'] == 1 and listing_info['inferredMoq'] == None:
            print(listing_info)
            orgId = listing_info['orgId']
            listingMoq = listing_info['listingMoq']
            inferredMoq = 1
            writer.writerow([orgId, listingMoq, inferredMoq])
            count += 1
        else:
            continue

t2 = time.time()
print('共统计 {} 件商品信息，共耗时 {} s'.format(str(count), str(t2 - t1)))
