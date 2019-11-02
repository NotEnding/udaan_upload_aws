#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/17 下午1:35
# ! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/4 下午2:43
import os, sys
import csv
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import LISTING_DB,CSV_FILE_PATH

listing_collection = LISTING_DB['listings_info']  # 商品表
org_collection = LISTING_DB['orgs_info']  # 店铺表
category_collection = LISTING_DB['categories_info']  # 品类表

'''
title:一级品类(页面展示名称)
targetId：一级品类(根据品类请求数据则用targetId，可理解为接口使用)
subCategories_id:二级品类id
subCategories_displayName：二级品类displayName(页面展示)
subCategories_subDisplayText：三级displayName集合
verticalInfoList_id：三级品类id
verticalInfoList_displayName：三级品类displayName(页面展示)
'''

t1 = time.time()
category_cursor = category_collection.find({})
print('开始获取 udaan 品类信息分析')
with open(CSV_FILE_PATH +'/udann品类信息分析.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ['title', 'targetId', 'subCategories_id', 'subCategories_displayName', 'subCategories_subDisplayText',
         'verticalInfo_id', 'verticalInfo_displayName'])
    count = 0
    for category_info in category_cursor:
        title = category_info['title']  # 一级品类 title
        targetId = category_info['targetId']  # 一级品类targetId
        for subCategories in category_info['subCategories']:
            subCategories_id = subCategories['id'] if subCategories['id'] else ''  # 二级品类id
            subCategories_displayName = subCategories['displayName'] if subCategories[
                'displayName'] else ''  # 二级品类displayName
            subCategories_subDisplayText = subCategories['subDisplayText'] if subCategories[
                'subDisplayText'] else ''  # 二级品类subDisplayText
            for verticalInfo in subCategories['verticalInfoList']:
                verticalInfo_id = verticalInfo['id'] if verticalInfo['id'] else ''  # 三级品类id
                verticalInfo_displayName = verticalInfo['displayName'] if verticalInfo[
                    'displayName'] else ''  # 三级品类displayName
                writer.writerow(
                    [title, targetId, subCategories_id, subCategories_displayName, subCategories_subDisplayText,
                     verticalInfo_id, verticalInfo_displayName])
        writer.writerow([title, targetId, '', '', '', '', ''])
        count += 1
t2 = time.time()
print('共统计 {} 种品类信息,共耗时 {} s'.format(str(count), str(t2 - t1)))
