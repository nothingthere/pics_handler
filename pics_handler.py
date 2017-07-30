#!/usr/bin/python3
# pics_handler.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-27 16:43:55
# Code:
'''
总入口
'''
import about_frame
import operation_frame
import os.path
import settings_frame
import sys
import tkinter as tk

ico = 'sdgs.ico'

root = tk.Tk()

#
# 初始窗口界面
#
root.title('山东高速集团四川产业运营公司鲜活车处理系统')
root.geometry('+10+10')
root.resizable(False, True)
if os.path.exists(ico) and 'win' in sys.platform:
    root.wm_iconbitmap(ico)

#
# 添加组件
#

settings = settings_frame.Frame(root)
settings.grid(column=0, row=0, sticky='nw', padx=(
    10, 10), pady=(10, 0), ipady=0)

about_frame.Frame(root).grid(column=0, row=1, sticky='w', padx=(10, 10))

operation_frame.Frame(root, settings).grid(
    column=1, row=0, rowspan=3, sticky='e', padx=(10, 10), pady=(0, 0))

#
# 运行
#


root.mainloop()
