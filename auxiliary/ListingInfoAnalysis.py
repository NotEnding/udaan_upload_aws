# -*- coding: utf-8 -*- 
# @Time : 2019/7/25 上午9:43 
# @Site :  
# @File : ListingInfoAnalysis.py
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
供应商id  供应商名称  供应商location  spu(listingId)  title(listing)  售价(?) gstPercent category(sellingCategories)
'''

t1 = time.time()  # 开始时间
listing_cursors = listing_collection.find({})  # 商品

with open(CSV_FILE_PATH + '/udaan供应商商品信息分析.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['供应商id', '供应商名称', '供应商location', 'spu', '商品title', '售价', 'gstPercent', 'category'])
    count = 0
    for listing_info in listing_cursors:
        orgId = listing_info['orgId']  # 供应商id
        orgName = listing_info['orgName']  # 供应商名称
        org_info = org_collection.find_one({"orgId": orgId}, {"location": 1, "sellingPrefs.sellingCategories": 1})
        category = org_info['sellingPrefs']['sellingCategories']  # category
        location = org_info['location']  # 供应商location
        spu = listing_info['listingId']  # spu(listingId)
        title = listing_info['title']  # title
        price_info = []
        for sales in listing_info['salesUnits']:
            for pricingConditions in sales['pricingConditions']:
                price_info.append(pricingConditions)  # 价格区间
        if not price_info:  # 如果price_info 为空
            minPricePaise = listing_info['minPricePaise']
            maxPricePaise = listing_info['maxPricePaise']
            if minPricePaise == maxPricePaise:
                print('111111111111111111111111111111111111111111111111111111111')
                # 构造字典
                price_info.append({
                    "minQty": sales['moq'],
                    "pricePaise": minPricePaise,
                    "maxQty": 2147483647
                })
            else:
                print('222222222222222222222222222222222222222222222222222222222')
                price_info.append(['未获得价格区间'])
        gstPercent = listing_info['gstPercent'] if listing_info['gstPercent'] else '0.00'  # 附加税
        writer.writerow([
            orgId, orgName, location, spu, title, price_info, gstPercent, category
        ])
        count += 1
        print(spu, count)
t2 = time.time()
print('共统计 {} 件商品信息，共耗时 {} s'.format(str(count), str(t2 - t1)))
