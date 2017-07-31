#!/usr/bin/python3
# settings.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-27 16:44:55
# Code:
'''
公共数据
'''

import datetime
import os
import time

FONT = {
    'family': 'Microsoft YaHei',
    'size': 12,
    'variant': 'normal'
}
IMAGE_FILE_EXTENSIONS = ['.jpeg', '.jpg', '.png']


def now():
    '返回当前日期时间。可用于伪造当前时间方便测试。'
    today = datetime.datetime.fromtimestamp(time.time())
    # delta = datetime.timedelta(days=1)
    # return today - delta
    return today


def datetime2date(dt):
    return datetime.datetime(year=dt.year, month=dt.month, day=dt.day)


def date_current():
    return datetime2date(now())


def filepaths_in_folder(folder):
    filenames_in_folder = os.listdir(path=folder)
    filepaths_in_folder = []
    for filename in filenames_in_folder:
        filepaths_in_folder.append(os.path.join(folder, filename))

    return filepaths_in_folder
