# -*- coding: utf-8 -*- 
# @Time : 2019/7/19 下午1:36 
# @Site :  
# @File : OrgInfoAnalysis.py
import os, sys
import csv
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import LISTING_DB,CSV_FILE_PATH

listing_collection = LISTING_DB['listings_info']  # 商品表
org_collection = LISTING_DB['orgs_info']  # 店铺表

'''
orgId displayName gstNumber gstAvailable location ownerName preferredContactNumber genneralPolicy sellingCategories yearInception
'''

t1 = time.time()
org_cursor = org_collection.find({})
print('开始获取udaan供应商信息分析')
with open(CSV_FILE_PATH +'/udaan供应商信息分析.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['orgId', 'displayName', 'gstNumber', 'gstnAvailable', 'location','locationCity','locationState','locationPincode','ownerName','preferredContactNumber','generalPolicy','sellingCategories','yearInception'])
    count = 0
    for org_info in org_cursor:
        orgId = org_info['orgId']
        print("正在统计店铺 {} 信息".format(orgId))
        displayName = org_info['displayName']
        gstNumber = org_info['gstNumber']
        gstnAvailable = org_info['gstnAvailable']
        location = org_info['location']
        locationCity = org_info['locationCity']
        locationState = org_info['locationState']
        locationPincode = org_info['locationPincode']
        ownerName = org_info['ownerName']
        preferredContactNumber = org_info['preferredContactNumber']
        generalPolicy = org_info['sellingPrefs']['generalPolicy']
        sellingCategories = org_info['sellingPrefs']['sellingCategories']
        yearInception = org_info['yearInception']
        writer.writerow([orgId,displayName,gstNumber,gstnAvailable,location,locationCity,locationState,locationPincode,ownerName,preferredContactNumber,generalPolicy,sellingCategories,yearInception])
        count += 1
t2 = time.time()
print('共统计 {} 家店铺信息,共耗时 {} s'.format(str(count), str(t2 - t1)))