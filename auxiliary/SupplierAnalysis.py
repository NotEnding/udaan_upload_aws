# -*- coding: utf-8 -*- 
# @Time : 2019/8/17 下午1:54 
# @Site :  
# @File : SupplierAnalysis.py
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
供应商id  供应商下面的产品总数 moq为1的产品总数 moq=1且pcs=1的产品总数  
'''

t1 = time.time()  # 开始时间
orgs_cursors = org_collection.find({}, {"orgId": 1})
listing_cursors = listing_collection.find({}, {"orgId": 1, "listingMoq": 1, "inferredMoq": 1})  # 商品

with open(CSV_FILE_PATH + '/udaan供应商商品moq分布情况分析.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['供应商id', '产品总数', 'moq为1的产品总数', 'moq=1且pcs=1的产品总数'])
    for org_info in orgs_cursors:
        org_count = listing_collection.find({"orgId": org_info['orgId']}).count()
        moq_count = 0
        moq_pcs_count = 0
        for listing_info in listing_collection.find({"orgId": org_info['orgId']}, {"listingMoq": 1, "inferredMoq": 1}):
            if listing_info['listingMoq'] == 1:
                moq_count += 1
                if listing_info['inferredMoq'] == None:
                    moq_pcs_count += 1
        writer.writerow([org_info['orgId'], org_count, moq_count, moq_pcs_count])
t2 = time.time()
print('共耗时 {} s'.format(str(t2 - t1)))
