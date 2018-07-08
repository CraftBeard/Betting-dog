#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 13:42:56 2018

@author: llx
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score

# 读取数据
laliga_data = pd.read_csv('/Users/llx/PyProjects/BettingDog/Data/Game Data/LaLiga_2011-2017.csv', encoding = 'gb2312')

# 数据清洗
# --清洗不同赛季当中的表头
laliga_data = laliga_data[laliga_data['轮次'] != '轮次']
laliga_data['轮次'] = laliga_data['轮次'].astype(int)

# --清洗列名
laliga_data['客队红牌'] = laliga_data['主队红牌.1'].astype(int)
laliga_data['主队红牌'] = laliga_data['主队红牌'].astype(int)

laliga_data['客队名称'] = laliga_data['主队名称.1']
laliga_data['客队名次'] = laliga_data['主队名次.1']
laliga_data = laliga_data.drop(['主队红牌.1', '主队名称.1', '主队名次.1'], axis = 1)

# 数据预处理
# --增加得分列
laliga_data['主队得分'] = laliga_data['比分'].str.split('-', 1, True)[0].astype(int)
laliga_data['客队得分'] = laliga_data['比分'].str.split('-', 1, True)[1].astype(int)

laliga_data['主队半场得分'] = laliga_data['半场比分'].str.split('-', 1, True)[0].astype(int)
laliga_data['客队半场得分'] = laliga_data['半场比分'].str.split('-', 1, True)[1].astype(int)

# --增加结果列(主队胜：2，主队负：1，平局：0)
laliga_data.loc[laliga_data['主队得分'] > laliga_data['客队得分'], '主队结果'] = 2
laliga_data.loc[laliga_data['主队得分'] < laliga_data['客队得分'], '主队结果'] = 1
laliga_data.loc[laliga_data['主队得分'] == laliga_data['客队得分'], '主队结果'] = 0

laliga_data.loc[laliga_data['主队结果'] == 2, '主队胜'] = 1
laliga_data.loc[laliga_data['主队结果'] < 2, '主队胜'] = 0

laliga_data['主队结果'] = laliga_data['主队结果'].astype(int)


# --增加比赛日期 按照 年 月 日 分开
laliga_data['比赛日期'] = pd.to_datetime(laliga_data['时间'].str[:10]).dt.strftime('%Y%m%d').astype(int)

laliga_data['比赛日期-年'] = laliga_data['比赛日期'].astype(str).str[:4].astype(int)
laliga_data['比赛日期-月'] = laliga_data['比赛日期'].astype(str).str[4:6].astype(int)
laliga_data['比赛日期-日'] = laliga_data['比赛日期'].astype(str).str[6:8].astype(int)
laliga_data['比赛日期-周'] = pd.to_datetime(laliga_data['比赛日期'], format='%Y%m%d').dt.weekday_name

# --计算当季球队进球，丢球数



# --增加近5场比赛胜率

# --增加近5场比赛主场胜率

# --增加近5场比赛客场胜率

# --增加近5场得分

# --增加近5场主场得分

# --增加近5场客场得分



# 保存到本地
# laliga_data.to_csv('/Users/llx/PyProjects/BettingDog/Data/Game Data/LaLiga_2013-2017_cleaned.csv')

# 特征工程
laliga_data.info()
laliga_data.describe()

# --相关性分析
laliga_data.corr()

# --IV值计算
# Calculate information value

# --PSI计算

# --WOE计算




# 计算相互对战战绩表
