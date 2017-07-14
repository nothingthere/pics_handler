#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-11 15:53:43
# Code:
'''
照片批量重命名程序
'''

import datetime
import functools
import os
import os.path
import re
import shutil
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
from collections import OrderedDict, namedtuple


class Application:
    def __init__(self, master):
        #
        # 公用部分
        #
        # 通用字体
        Font = namedtuple('Font', 'family, size, variant')
        self.font = Font('Arial', 12, 'normal')  # 通用字体
        # if 'win' in sys.platform:
        #     self.font.family = 'Microsoft Yahei UI'

        self._padx = 5          # 通用外间距
        self._pady = 5

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
            row=0, column=0, sticky='nw', padx=10)
        self.about_frame.grid(row=1, column=0, sticky='nw', padx=10, pady=10)
        self.dir_frame.grid(row=0, column=1, sticky='ne')

        self.cars_yesterday = tk.StringVar()             # 昨天车辆数量
        self.cars_yesterday_edited = tk.StringVar()        # 昨天已经编辑好车辆数
        self.pics_per_car = 3               # 每辆车照片数量
        self.inplace = tk.BooleanVar()        # 是否修改当前文件夹
        self._dir = tk.StringVar()            # 照片所在文件夹
        self._dir_suffix = '.NEW'                # 新建文件夹后缀

        self.cars_yesterday.set('0')
        self.cars_yesterday_edited.set('')
        self.inplace.set(False)

        #
        # setting_frame
        #

        # 昨天车辆数量
        tk.Label(self.setting_frame, cnf={
            'text': '昨天未编辑车辆数：',
            'font': self.font,
        }).grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.cars_yesterday_entry = tk.Entry(self.setting_frame, cnf={
            'textvariable': self.cars_yesterday,
            'width': '5',
            'font': self.font,
        })
        self.cars_yesterday_entry.grid(row=0, column=1, sticky='e', padx=10)

        # 输入后按下回车键，如果数字合法，则可编辑“昨天已编辑好车辆数”
        self.cars_yesterday_entry.bind(
            '<Return>', self.enable_cars_yesterday_cars_yesterday_edited_entry)
        # 跳过昨天车辆数
        tk.Label(self.setting_frame, cnf={
            'text': '昨天已编辑好车辆数：',
            'font': self.font,
        }).grid(row=1, column=0, sticky='w', padx=5, pady=5)

        self.cars_yesterday_edited_entry = ttk.Entry(self.setting_frame,
                                                     textvariable=self.cars_yesterday_edited,
                                                     width=5,
                                                     font=self.font,
                                                     state=['disabled']
                                                     )
        self.cars_yesterday_edited_entry.grid(
            row=1, column=1, sticky='e', padx=10)

        self.cars_yesterday_edited_entry.bind(
            '<Return>', self.focus_inplace_checkbutton)

        # 是否在当前文件夹中修改
        tk.Label(self.setting_frame, cnf={
            'text': '是否在当前文件夹中修改：',
            'font': self.font,
        }).grid(row=2, column=0, sticky='w', padx=5, pady=5)

        self.inplace_checkbutton = tk.Checkbutton(self.setting_frame, cnf={
            'variable': self.inplace,
            'onvalue': True,
            'offvalue': False,
        })
        self.inplace_checkbutton.grid(
            row=2, column=1, sticky='e', pady=5, padx=10)

        #
        # about_frame
        #

        for i, text in enumerate(['Version: 0.2.1',
                                  'Author: claudio',
                                  'Contact: 3261958605@qq.com']):
            tk.Label(self.about_frame, cnf={
                'text': text,
                'font': (self.font.family, self.font.size - 2, 'italic')
            }).grid(row=i, column=0, sticky='w')

        #
        # dir_frame
        #
        tk.Label(self.dir_frame, cnf={
            'text': '请选择文件夹：',
            'font': (self.font.family, self.font.size + 2, 'italic'),
        }).grid(row=0, column=0, columnspan=2, sticky='w')

        tk.Entry(self.dir_frame, cnf={
            'width': 30,
            'textvariable': self._dir,
            'font': (self.font.family, self.font.size + 2)
        }).grid(row=1, column=0, sticky='w')

        tk.Button(self.dir_frame, cnf={
            'text': '选择',
            'font': (self.font.family, self.font.size + 1),
            'command': self.select_dir,
        }).grid(row=1, column=1, sticky='e', padx=10)

        # 提交按钮
        tk.Button(self.dir_frame, cnf={
            'text': '执行',
            'font': (self.font.family, self.font.size + 2, 'bold'),
            'command': self.rename,
        }).grid(row=2, column=0, columnspan=2, pady=5)

        # 进度条
        self.progress = tk.IntVar()

        self.progressbar = ttk.Progressbar(self.dir_frame,
                                           mode='determinate',
                                           orient=tk.HORIZONTAL,
                                           length=300,
                                           variable=self.progress,
                                           )
        self.progressbar.grid(row=3, column=0, columnspan=2, pady=10)

    def enable_cars_yesterday_cars_yesterday_edited_entry(self, _event):
        '''
        如果对“昨天车辆数输入合法”，按下回车则聚焦到输入“昨天已经编辑好车辆数”的输入文本框，
        否则弹出警告。
        '''
        cars_yesterday = self.check_num_input_entry(self.cars_yesterday.get())
        if isinstance(cars_yesterday, str):
            self.cars_yesterday_edited.set('')
            self.cars_yesterday_edited_entry.state(['disabled'])
            self.show_error(cars_yesterday)
        else:
            self.cars_yesterday_edited_entry.state(['!disabled'])
            self.cars_yesterday_edited_entry.focus()

    def focus_inplace_checkbutton(self, _event):
        '''
        如果对“昨天已经编辑好车辆数”输入合法，
        按下回车则聚焦到选择“是否在当前文件夹中修改”的选择框
        '''
        cars_yesterday_edited = self.check_num_input_entry(
            self.cars_yesterday_edited.get())
        if isinstance(cars_yesterday_edited, str):
            self.show_error(cars_yesterday_edited)
        else:
            self.inplace_checkbutton.focus()

    def show_error(self, msg):
        messagebox.showerror(title='错误', message=msg)
        self.progress.set(0)

    def increase_progress(self, num=1):
        value = self.progress.get()
        self.progress.set(value + num)

    def select_dir(self):
        dir_name = filedialog.askdirectory()
        self._dir.set(dir_name)
        # self.entry.delete(0, tk.END)
        # self.entry.insert(0, dir_name)

    def validate_dirpath(self, dirname):
        '''如果不是文件夹或文件夹中不含图片文件，或
        图片数量不为设置的整数倍，返回消息字符串；
        如果检查通过，返回图片文件路径组成的链表
        '''''
        image_files = []

        if not dirname:
            return '请选择文件夹先'
        if not os.path.exists(dirname):
            return '{}：不存在此文件件'.format(dirname)
        if not os.path.isdir(dirname):
            return '{}: 不为文件夹'.format(dirname)

        for dirpath, _dirname, filenames in os.walk(dirname):
            for filename in filenames:
                filetype = os.path.splitext(filename)[1][1:]
                if filetype and filetype.lower() in ['jpeg', 'jpg', 'png']:
                    image_files.append(os.path.join(dirpath, filename))

        return image_files

    def alphanum_key(self, image_file_path, regex=re.compile(r'\d+')):
        '''
        排序按字母顺序排列的文件路径名，
        默认为统一文件夹中的文件名，
        排序方法：先尝试使用数字大小，否则按字母顺序，
        不然10001会小于1001
        '''
        filename = os.path.basename(image_file_path)
        filename = os.path.splitext(filename)[0]
        nums = regex.findall(filename)
        # print(nums)
        if nums:
            return functools.reduce(lambda x, y: x + int(y), nums, 0)
        else:
            return filename

    def sort_image_file_paths(self, image_file_paths):
        '''
        排序图片文件路径组成的序列
        @ image_file_paths：需排序的图片文件路径组成的序列。

        排序方法：
        1. 对于普通文件名，按字母顺序排序
        2. 对于"1[xX]2[.jpeg]"名称的文件名，“1”表示第1辆车，“2”表示第1辆车的第2张图片。

        否则返回排序好的路径组成序列。
        '''
        # 正常名称路径组成的序列
        normal_paths = []
        # key为特殊路径名，value为car_index和pic_index组成的命名元组
        special_paths = dict()

        regex = re.compile(
            r'.*[^0-9](?P<car_index>\d+)[xX](?P<pic_index>[0-9]+)(?:.[jpeg|png|gif])?', re.IGNORECASE)

        for path in image_file_paths:
            mo = regex.match(path)
            if mo:
                # print(mo.groupdict())
                car_index = int(mo.group('car_index'))
                pic_index = int(mo.group('pic_index'))
                # print(path, len(image_file_paths) / self.pics_per_car,
                #       'car_index:', car_index, 'pic_index:', pic_index)

                if car_index > len(image_file_paths) / self.pics_per_car\
                   or pic_index > self.pics_per_car:
                    return '{}：文件名有误，请重命名该文件'.format(path)

                special_paths[path] = (car_index - 1) * \
                    self.pics_per_car + (pic_index - 1)
            else:
                normal_paths.append(path)

        normal_paths.sort(key=self.alphanum_key)

        # 如果不使用OrderedDict会造成插入混乱
        special_paths = OrderedDict(
            sorted(special_paths.items(), key=lambda x: x[1]))

        for path, index in special_paths.items():
            normal_paths.insert(index, path)

        return normal_paths

    def _rename(self, image_file_paths, new_folder_path, days=0,
                inplace=False, cars_yesterday_edited=0):
        '''
        重命名操作函数。

        为防止在同一文件夹中重命名时（inplace参数为True）文件名发生冲突，
        如果新名称已存于当前文件夹，如201712-2002.jpg,需重命名为201712-1002.jpg，
        则将其重命名为201712-1002.jpg._new
        遍历image_file_paths后再将其重命名为为应该有的名称201712-1002.jpg

        @image_files_paths：排序后的图片文件路径名称链表

        @new_folder_path：图片放置位置

        @days：整数，-1表示向前一天

        @inplace：是否修改当前文件夹

        @cars_yesterday_edited：昨天已编辑好车辆数

        '''
        index = 1
        cars = cars_yesterday_edited + 1
        new_path = ''
        today = datetime.date.today()
        day_delta = datetime.timedelta(days=days)
        today += day_delta

        prefix = '{}{:02}{:02}'.format(
            today.year, today.month, today.day)
        suffix = ''

        extension = ''
        duplicated_file_paths = []
        # print('-' * 20)

        for image_file_path in image_file_paths:
            # 获取原来文件名后缀
            extension = os.path.splitext(image_file_path)[1]
            suffix = '{:03}-{}{}'.format(cars, index, extension)
            new_path = os.path.join(new_folder_path,  prefix + suffix)
            # print(new_path)
            index += 1
            if index > self.pics_per_car:
                index = 1
                cars += 1

            if inplace:
                if new_path in image_file_paths:
                    duplicated_file_paths.append(new_path)
                    # print(image_file_path, ' --> ', new_path + '_new')
                    shutil.move(image_file_path, new_path + '_new')
                else:
                    # print(image_file_path, ' --> ', new_path)
                    shutil.move(image_file_path, new_path)
            else:
                # print(image_file_path, ' --> ', new_path)
                shutil.copy2(image_file_path, new_path)

        self.increase_progress(len(image_file_paths))
        return duplicated_file_paths

    def check_num_input_entry(self, str_var):
        '''
        检查Entry中输入是否合法，
        如果合法，返回对应数值，
        否则返回小写字符串。
        '''
        num = str_var.strip()
        try:
            if num == '':
                return 0
            return int(num)
        except ValueError:
            return '请使用纯数字设置车辆数'

    def rename(self):
        '''
        获取配置，并检查配置是否合法，
        如果不合法，终止于此
        如果合法，则调用核心函数_rename
        '''
        self.progress.set(1)
        #
        # 获取设置
        #

        cars_yesterday = self.cars_yesterday.get()
        cars_yesterday_edited = self.cars_yesterday_edited.get()
        inplace = self.inplace.get()
        dirname = self._dir.get()
        new_dirname = dirname   # 重命名后图片放置文件夹
        image_file_paths = []   # 照片路径
        image_file_num = 0      # 照片数量
        #
        # 检查设置是否合法
        #
        cars_yesterday = self.check_num_input_entry(cars_yesterday)
        if isinstance(cars_yesterday, str):
            self.show_error(cars_yesterday)
            return
        cars_yesterday_edited = self.check_num_input_entry(
            cars_yesterday_edited)
        if isinstance(cars_yesterday_edited, str):
            self.show_error(cars_yesterday_edited)
            return
        # try:
        #     cars_yesterday = cars_yesterday.strip()
        #     if not cars_yesterday:
        #         cars_yesterday = 0
        #     else:
        #         cars_yesterday = int(cars_yesterday)
        # except ValueError:
        #     self.show_error("请使用纯数字设置车辆数")
        #     return

        image_file_paths = self.validate_dirpath(dirname)
        if isinstance(image_file_paths, str):
            self.show_error(image_file_paths)
            return
        else:
            image_file_num = len(image_file_paths)
            self.progressbar.config(maximum=image_file_num)
            if image_file_num == 0:
                self.show_error('{}：无图片文件'.format(dirname))
                return
            if cars_yesterday * self.pics_per_car > image_file_num:
                self.show_error('昨天车辆数是否有误：{} x 3 > {}？'.format(
                    cars_yesterday, image_file_num))
                return
            if image_file_num % self.pics_per_car != 0:
                self.show_error('{}：照片数量不为3的整数倍。图片张数为：{}'.format(
                    dirname, image_file_num))
                return

            image_file_paths = self.sort_image_file_paths(image_file_paths)
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
                                       message='{}：已存在，是否删除？'.format(new_dirname)):
                    # print('删除文件夹：', new_dirname)
                    # 先删除，再创建，相当于清空文件夹
                    shutil.rmtree(new_dirname)
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
        # '''.format(cars_yesterday, cars_yesterday_edited, inplace, dirname, new_dirname, image_file_num))

        #
        # 执行重命名
        #

        duplicate_paths = []
        duplicate_paths.extend(self._rename(image_file_paths[:cars_yesterday * self.pics_per_car],
                                            new_dirname, days=-1, inplace=inplace, cars_yesterday_edited=cars_yesterday_edited))
        duplicate_paths.extend(self._rename(image_file_paths[cars_yesterday * self.pics_per_car:],
                                            new_dirname, days=0, inplace=inplace))

        for file_path in duplicate_paths:
            os.rename(file_path + '_new', file_path)

        # import time
        # time.sleep(1)
        # self.progressbar.stop()
        #
        # 提示操作成功
        #
        messagebox.showinfo(
            title='成功',
            message='操作成功，重命名后图片所在位置：' + new_dirname
        )

#
# MAIN
#


def main():
    root = tk.Tk()
    root.title('鲜活照片批量处理程序')
    root.geometry('+20+20')
    root.resizable(False, False)

    Application(root)

    root.mainloop()


main()
