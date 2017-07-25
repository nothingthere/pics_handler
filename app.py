#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-15 10:16:15
# Code:
'''
照片批量重命名
'''


import os
import os.path
import shutil
import sys
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import utils
import webbrowser
from collections import namedtuple


class Application:
    def __init__(self, master):
        self.master = master
        #
        # 公用部分
        #
        # 通用字体
        Font = namedtuple('Font', 'family, size, variant')
        self.font = Font('Arial', 12, 'normal')  # 通用字体
        self.manual_url = r'https://github.com/nothingthere/pics_handler/blob/master/README.org'
        #
        # Frame
        #

        self.setting_frame = tk.LabelFrame(master, cnf={  # 获取设置
            'text': '设置',
            'font': (self.font.family, self.font.size + 2),
        })
        self.about_frame = tk.Frame(master)    # 关于此软件
        self.dir_frame = tk.Frame(master)     # 获取文件夹

        self.setting_frame.grid(
            row=0, column=0, sticky='nw', padx=(10, 10))
        self.about_frame.grid(row=1, column=0, sticky='nw',
                              padx=10, pady=(10, 20))
        self.dir_frame.grid(row=0, column=1, rowspan=2,
                            sticky='ne', padx=(10, 10))

        self.cars_yesterday = tk.StringVar()             # 昨天车辆数量
        self.cars_yesterday_edited = tk.StringVar()        # 昨天已经编辑好车辆数
        self.pics_per_car = 3               # 每辆车照片数量
        self.inplace = tk.BooleanVar()        # 是否修改当前文件夹
        self._dir = tk.StringVar()            # 照片所在文件夹
        self._dir_suffix = '.NEW'                # 新建文件夹后缀

        self.cars_yesterday.set('0')
        self.cars_yesterday_edited.set('0')
        self.inplace.set(True)

        #
        # setting_frame
        #

        # 昨天车辆数量
        tk.Label(self.setting_frame, cnf={
            'text': '昨天（未）编辑车辆数：',
            'font': self.font,
        }).grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.cars_yesterday_entry = tk.Entry(
            self.setting_frame,
            textvariable=self.cars_yesterday,
            width='5',
            font=self.font,
        )
        self.cars_yesterday_entry.grid(row=0, column=1, sticky='e', padx=10)

        # 输入后按下回车键，如果数字合法，则可编辑“昨天已编辑好车辆数”
        # self.cars_yesterday_entry.bind(
        #     '<Return>', self.enable_cars_yesterday_cars_yesterday_edited_entry)
        # 跳过昨天车辆数
        tk.Label(self.setting_frame, cnf={
            'text': '昨天（已）编辑车辆数：',
            'font': self.font,
        }).grid(row=1, column=0, sticky='w', padx=5, pady=5)

        self.cars_yesterday_edited_entry = tk.Entry(
            self.setting_frame,
            textvariable=self.cars_yesterday_edited,
            width=5,
            font=self.font,
            # state='disabled',
        )

        # self.cars_yesterday_edited_entry.bind(
        #     '<Button-1>',
        #     self.enable_cars_yesterday_cars_yesterday_edited_entry)

        self.cars_yesterday_edited_entry.grid(
            row=1, column=1, sticky='e', padx=10)

        # self.cars_yesterday_edited_entry.bind(
        #     '<Return>', self.focus_inplace_checkbutton)

        # 是否在当前文件夹中修改
        tk.Label(self.setting_frame, cnf={
            'text': '是否在当前文件夹中修改：',
            'font': self.font,
        }).grid(row=2, column=0, sticky='w', padx=5, pady=5)

        self.inplace_checkbutton = tk.Checkbutton(
            self.setting_frame,
            variable=self.inplace,
            onvalue=True,
            offvalue=False,
        )
        self.inplace_checkbutton.grid(
            row=2, column=1, sticky='e', pady=5, padx=10)

        #
        # about_frame
        #

        for i, text in enumerate(['Version: 0.3.1',
                                  'Author: claudio',
                                  'Contact: 3261958605@qq.com']):
            tk.Label(self.about_frame, cnf={
                'text': text,
                'font': (self.font.family, self.font.size - 2, 'italic')
            }).grid(row=i, column=0, sticky='w')

        # 使用说明
        self.manual = tk.Label(self.about_frame, cnf={
            'text': "使用说明",
            'font': (self.font.family, self.font.size - 2, 'italic underline'),
            'fg': 'blue',
            'cursor': 'hand2',
        })

        self.manual.grid(row=3, column=0, sticky='w')
        self.manual.bind(
            '<Button-1>', lambda e: webbrowser.open_new(self.manual_url))

        # logo图标
        self.logo = tk.PhotoImage(file='sdgs.gif')
        self.logo_label = tk.Label(self.about_frame)
        self.logo_label.config(image=self.logo, compound='right')
        self.logo_label.grid(row=0, column=1, rowspan=4, padx=(20, 0))

        #
        # dir_frame
        #

        tk.Label(self.dir_frame, cnf={
            'text': '请选择文件夹：',
            'font': (self.font.family, self.font.size + 2, 'italic'),
        }).grid(row=0, column=0, sticky='w')

        self.dir_entry = tk.Entry(self.dir_frame, cnf={
            'width': 30,
            'textvariable': self._dir,
            'font': (self.font.family, self.font.size + 2)
        })
        self.dir_entry.grid(row=1, column=0, sticky='w')

        self.chose_dir_button = tk.Button(
            self.dir_frame,
            text='选择',
            font=(self.font.family, self.font.size + 1),
            command=self.select_dir,
        )
        self.chose_dir_button.grid(row=1, column=1, sticky='e', padx=(10, 0))

        # 提交按钮
        self.submit_button = tk.Button(
            self.dir_frame,
            text='执行',
            font=(self.font.family, self.font.size + 2, 'bold'),
            command=self.rename,
        )
        self.submit_button.grid(row=2, column=0,
                                columnspan=2, pady=(30, 0))

        # 进度条（这是一个虚假的进度条）
        self.progress = tk.StringVar()
        self.progress.set('')
        self.progress_label = tk.Label(self.dir_frame, cnf={
            'textvariable': self.progress,
            'width': 10,
            'height': 1,
            'font': (self.font.family, self.font.size + 1, 'italic'),
        })

        self.progress_label.grid(row=3, columnspan=2, pady=(20, 0))

    def diable_all_interactive(self):
        '禁用所有交互'
        self.cars_yesterday_entry.configure(state='disabled')
        self.cars_yesterday_edited_entry.configure(state='disabled')
        self.inplace_checkbutton.configure(state='disabled')
        self.chose_dir_button.configure(state='disabled')
        self.dir_entry.configure(state='disabled')
        self.submit_button.configure(state='disabled')

    def enable_all_interactive(self):
        '启用所有交互'
        self.cars_yesterday_entry.configure(state='normal')
        self.cars_yesterday_edited_entry.configure(state='normal')
        self.inplace_checkbutton.configure(state='normal')
        self.dir_entry.configure(state='normal')
        self.chose_dir_button.configure(state='normal')
        self.submit_button.configure(state='normal')

    def step_progress(self, msg):
        self.progress.set(msg)

    # def enable_cars_yesterday_cars_yesterday_edited_entry(self, _event):
    #     '''
    #     如果对“昨天车辆数输入合法”，
    #     按下回车则聚焦到输入“昨天已经编辑好车辆数”的输入文本框，
    #     否则弹出警告。
    #     '''
    #     cars_yesterday = utils.validate_num_input(self.cars_yesterday.get())
    #     if isinstance(cars_yesterday, str):
    #         self.cars_yesterday_edited.set('')
    #         self.cars_yesterday_edited_entry.configure(state='disabled')
    #         self.show_error(cars_yesterday)
    #     else:
    #         self.cars_yesterday_edited_entry.configure(state='normal')
    #         self.cars_yesterday_edited_entry.focus()

    # def focus_inplace_checkbutton(self, _event):
    #     '''
    #     如果对“昨天已经编辑好车辆数”输入合法，
    #     按下回车则聚焦到选择“是否在当前文件夹中修改”的选择框
    #     '''
    #     cars_yesterday_edited = utils.validate_num_input(
    #         self.cars_yesterday_edited.get())

    #     if isinstance(cars_yesterday_edited, str):
    #         self.show_error(cars_yesterday_edited)
    #     else:
    #         self.inplace_checkbutton.focus()

    def show_error(self, msg):
        self.step_progress('')
        messagebox.showerror(title='错误', message=msg)

    def select_dir(self):
        dir_name = filedialog.askdirectory()
        self._dir.set(dir_name)

    def rename(self):
        '''
        获取配置，并检查配置是否合法，
        如果不合法，终止于此
        如果合法，则调用核心函数_rename
        '''
        #
        # 获取设置
        #

        cars_yesterday = self.cars_yesterday.get()
        cars_yesterday_edited = self.cars_yesterday_edited.get()
        inplace = self.inplace.get()
        dirname = self._dir.get()
        new_dirname = dirname   # 重命名后图片放置文件夹
        image_file_paths = []   # 照片路径
        images_yesterday = []  # 昨天照片
        images_today = []     # 今天照片
        new_file_paths = []       # 重命名后照片路径组成的序列
        rename_func = shutil.copy  # 执行重命名的函数
        #
        # 检查设置是否合法
        #
        cars_yesterday = utils.validate_num_input(cars_yesterday)
        if isinstance(cars_yesterday, str):
            self.show_error(cars_yesterday)
            return

        cars_yesterday_edited = utils.validate_num_input(cars_yesterday_edited)
        if isinstance(cars_yesterday_edited, str):
            self.show_error(cars_yesterday_edited)
            return

        image_file_paths = utils.validate_images_folder(dirname)
        if isinstance(image_file_paths, str):
            self.show_error(image_file_paths)
            return

        if cars_yesterday * 3 > len(image_file_paths):
            self.show_error('{}：昨天车辆数对应照片数大于文件夹中照片数'.format(dirname))
            return

        image_file_paths = utils.sort_image_file_paths(image_file_paths)
        if isinstance(image_file_paths, str):
            self.show_error(image_file_paths)
            return

        #
        # 获取图片重命名后放置文件夹：
        # 如果不为修改当前文件夹，且已经存在，询问是否删除
        # 如果不存在，则创建
        #
        if not inplace:
            new_dirname = dirname + self._dir_suffix
            # print(new_dirname)
            if os.path.exists(new_dirname) and os.path.isdir(new_dirname):
                # print('存在且为文件夹')
                if messagebox.askyesno(title='提示',
                                       message='{}：已存在，是否清空？'.format(new_dirname)):
                    # print('删除文件夹：', new_dirname)
                    # 先删除，再创建，相当于清空文件夹
                    try:
                        shutil.rmtree(new_dirname)
                    except:
                        self.show_error(
                            '{}：可能被另一个程序占用。清空失败'.format(new_dirname))
                        return
                    os.makedirs(new_dirname)
                else:
                    return
            else:
                # print('创建文件夹：', new_dirname)
                os.makedirs(new_dirname)

        # print('''
        # 昨天车辆数：{}
        # 昨天已经编辑好车辆数：{}
        # 是否在当前文件夹修改：{}
        # 选择的图片文件夹：{}
        # 重命名后图片放置文件夹：{}
        # 图片个数：{}
        # '''.format(cars_yesterday, cars_yesterday_edited, inplace, dirname, new_dirname, len(image_file_paths)))

        #
        # 执行重命名
        #
        self.diable_all_interactive()
        self.step_progress('处理中...')
        # 如需创建目标文件夹，界面不会自动刷新，
        # 所以调用update_idletasks()手动刷新
        self.master.update_idletasks()

        images_yesterday = image_file_paths[:
                                            cars_yesterday * self.pics_per_car]
        images_today = image_file_paths[cars_yesterday * self.pics_per_car:]
        if inplace:
            rename_func = os.rename

        # 执行对昨天的车辆数重命名
        new_file_paths = utils.construct_new_names(images_yesterday,
                                                   new_dirname, days=-1, skip=cars_yesterday_edited)
        utils.move_files(images_yesterday, new_file_paths, func=rename_func)
        if inplace:
            utils.move_files(
                *utils.construct_resolution_new_names(new_file_paths), func=rename_func)

        # 对今天的车辆重命名
        new_file_paths = utils.construct_new_names(images_today, new_dirname)
        utils.move_files(images_today, new_file_paths, func=rename_func)
        if inplace:
            utils.move_files(
                *utils.construct_resolution_new_names(new_file_paths), func=rename_func)

        #
        # 提示操作成功
        #
        self.step_progress('')
        self.enable_all_interactive()
        messagebox.showinfo(
            title='成功',
            message='操作成功，重命名后图片所在位置：' + new_dirname
        )

#
# MAIN
#


def main():
    root = tk.Tk()
    ico = 'sdgs.ico'

    root.title('鲜活照片批量重命名')
    root.geometry('+20+20')
    root.resizable(False, False)

    if os.path.exists(ico) and 'win' in sys.platform:
        root.wm_iconbitmap(ico)

    Application(root)

    root.mainloop()


main()
