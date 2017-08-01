#!/usr/bin/python3
# setting_frame.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-27 16:42:00
# Code:
'''
设置界面组件
'''

import tkinter as tk
from public import FONT


class Frame(tk.LabelFrame):
    def __init__(self, master):
        super(Frame, self).__init__(master)
        self.font = (FONT['family'], FONT['size'], FONT['variant'])

        self.config(text='选项', font=(self.font[0], self.font[1] + 2, 'normal'))

        self.edited = tk.StringVar()
        self.edited.set('0')
        self.edited_widget = None

        self.default_lane = tk.StringVar()
        self.default_lane.set(7)
        self.default_lane_widget = None

        # self.add_edited()
        self.add_default_lane()

    def add_edited(self):
        tk.Label(self,
                 text='已编辑昨天车辆数：',
                 font=self.font,
                 ).grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.edited_widget = tk.Entry(self,
                                      font=self.font,
                                      width=4,
                                      textvariable=self.edited,
                                      )
        self.edited_widget.grid(
            row=0, column=1, sticky='e', padx=5, pady=5)

    def add_default_lane(self):
        tk.Label(self,
                 text='鲜活车常过车道：',
                 font=self.font,
                 ).grid(row=2, column=0, sticky='w', padx=5, pady=20)

        self.default_lane_widget = tk.Spinbox(self,
                                              from_=1, to=20,
                                              textvariable=self.default_lane,
                                              font=self.font,
                                              width=3,
                                              )

        self.default_lane_widget.grid(
            row=2, column=1, sticky='e', padx=5, pady=20)

    def disable_interactive(self):
        # self.edited_widget.configure(state='disabled')
        self.default_lane_widget.configure(state='disabled')

    def enable_interactive(self):
        # self.edited_widget.configure(state='normal')
        self.default_lane_widget.configure(state='normal')
