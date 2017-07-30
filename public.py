#!/usr/bin/python3
# settings.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-27 16:44:55
# Code:
'''
公共数据
'''

import datetime
import time

FONT = {
    'family': 'Microsoft YaHei',
    'size': 12,
    'variant': 'normal'
}


def now():
    today = datetime.datetime.fromtimestamp(time.time())
    # 为方便测试，或以后添加向后缩减一天的功能
    # yesterday = today - datetime.timedelta(days=1)
    return today
    # return yesterday


def datetime2date(dt):
    return datetime.datetime(year=dt.year, month=dt.month, day=dt.day)


def date_current():
    return datetime2date(now())
