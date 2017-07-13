#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-13 14:09:45
# Code:
'''
对app.py的测试
'''

import tkinter as tk
from app import Application

#
# 测试对图片的获取和排序
#

app = Application(tk.Tk())
dirname = '/home/claudio/Desktop/Python/pics-handler/test_pics'
image_file_paths = app.validate_dirpath(dirname)


def show_files():
    print('图片个数：', len(image_file_paths))
    for i, file in enumerate(image_file_paths):
        print(i, file)


image_file_paths = app.sort_image_file_paths(image_file_paths)
show_files()


#
# 测试重命名
#
