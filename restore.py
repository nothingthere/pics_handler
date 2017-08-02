#!/usr/bin/python3
# restore.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-08-01 19:01:50
# Code:
'''
记录和加载上次配置：
默认车道、源文件件、目标文件件、Excel文件路径
'''


import json
import os.path

FILE = 'configuration.json'


def load(tk_default_lanne, tk_src_folder, tk_dst_folder, tk_excel_file):
    if not os.path.exists(FILE):
        with open(FILE, 'w') as _fp:
            pass
        return

    config = dict()

    try:
        with open(FILE, 'r') as fp:
            config = json.load(fp)
    except:
        pass

    default_lane = config.get('default_lane')
    src_folder = config.get('src_folder')
    dst_folder = config.get('dst_folder')
    excel_file = config.get('excel_file')

    if config:
        if default_lane:
            tk_default_lanne.set(str(default_lane))

        if src_folder:
            tk_src_folder.set(src_folder)

        if dst_folder:
            tk_dst_folder.set(dst_folder)

        if excel_file:
            tk_excel_file.set(excel_file)


def dump(default_lanne, src_folder, dst_folder, excel_file):
    if not os.path.exists(FILE):
        with open(FILE, 'w') as _fp:
            pass

    config = dict()

    config['default_lane'] = default_lanne
    config['src_folder'] = src_folder
    config['dst_folder'] = dst_folder
    config['excel_file'] = excel_file

    try:
        with open(FILE, 'w') as fp:
            json.dump(config, fp, ensure_ascii=False)
    except:
        pass
