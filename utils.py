#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-14 21:51:59
# Code:
'''
工具函数
'''
import concurrent.futures as cf
import datetime
import functools
import os.path
import re
import shutil
from collections import OrderedDict


def validate_num_input(str_var):
    '''
    检查Entry中输入是否合法，

    如果合法，返回对应数值,

    如果去除空白字符后为空，则返回0

    否则返回消息字符串。

    '''
    num = str_var.strip()
    try:
        if num == '':
            return 0
        return int(num)
    except ValueError:
        return '请使用纯数字设置车辆数'


def validate_images_folder(dirname, n=3):
    '''
    放置图片的文件夹


    如果不是文件夹或文件夹中不含图片文件，或
    图片数量不为设置的整数倍，返回消息字符串；
    如果检查通过，返回图片文件路径组成的链表

    缺点：只根据文件名后缀判断是否为图片文件


    @dirname：文件夹路径
    @n：图片数量是否为n的整数倍
    '''
    image_files = []
    image_file_extensions = ['jpeg', 'jpg', 'png']

    if not dirname:
        return '请选择文件夹先'
    if not os.path.exists(dirname):
        return '{}：不存在此文件夹'.format(dirname)
    if not os.path.isdir(dirname):
        return '{}: 不为文件夹'.format(dirname)

    for dirpath, _dirname, filenames in os.walk(dirname):
        for filename in filenames:
            filetype = os.path.splitext(filename)[1][1:]
            if filetype and filetype.lower() in image_file_extensions:
                image_files.append(os.path.join(dirpath, filename))

    if len(image_files) == 0:
        return '{}：无图片文件'.format(dirname)

    if len(image_files) % n != 0:
        return '{}：图片数量不为{}的整数倍'.format(dirname, n)

    return image_files


def move_files(old_names, newnames, func=shutil.copy):
    '''
    理由多线程复制/或重命名文件
    默认为复制文件，及使用shutil.copy
    可使用shutil.move实现重命名
    '''
    # def func(x, y):
    #     pass
    # print(x, ' --> ', y)
    with cf.ThreadPoolExecutor() as e:
        e.map(func, old_names, newnames)


def construct_new_names(old_paths, new_dir, days=0, skip=0, n=3, resolution='_new'):
    '''
    重命名操作函数。

    为防止在同一文件夹中重命名时（inplace参数为True）文件名发生冲突，
    如果新名称已存于当前文件夹，如201712-2002.jpg,需重命名为201712-1002.jpg，
    则将其重命名为201712-1002.jpg._new
    遍历image_file_paths后再将其重命名为为应该有的名称201712-1002.jpg

    返回结果：新路径名组成的序列

    @old_paths：需重命名的文件路径序列

    @new_dir：新文件夹路径

    @days：整数，-1表示向前一天

    @inplace：是否修改当前文件夹

    @skip：昨天已编辑好车辆数，如果days=-1，则从skip+1开始编号车辆数

    @n：每辆车的图片个数

    @resolution：当新名称存在于存在于需重命名的文件路径序列中时
    （仅在当前文件夹中修改时有可能发送），
    新名称后添加的识别字符串。

    '''

    index = 1                   # 图片编号
    cars = skip + 1               # 车辆编号
    today = datetime.date.today()   # 今天日期
    day_delta = datetime.timedelta(days=days)
    today += day_delta

    new_path = ''            # 新的完整路径名
    new_file_name = ''
    extension = ''

    result = []    # 返回结果

    for path in old_paths:
        extension = os.path.splitext(path)[1]

        new_file_name = '{}{:02}{:02}'.format(
            today.year, today.month, today.day)
        new_file_name += '{:03}-{}{}'.format(cars, index, extension)

        index += 1
        if index > n:
            index = 1
            cars += 1

        new_path = os.path.join(new_dir, new_file_name)

        if new_path in old_paths:
            result.append(new_path + resolution)
        else:
            result.append(new_path)

    return result


def construct_resolution_new_names(paths, resolution='_new'):
    result = [[], []]
    for p in paths:
        if p.endswith(resolution):
            result[0].append(p)
            result[1].append(p.rstrip(resolution))
        # else:
        #     print(p)

    return result


def alphanum_key(image_file_path, regex=re.compile(r'\d+')):
    '''
    排序按字母顺序排列的文件路径名，
    默认为统一文件夹中的文件名，
    排序方法：先尝试使用数字大小，否则按字母顺序，
    不然10001会小于1001
    '''
    filename = os.path.basename(image_file_path)
    filename = os.path.splitext(filename)[0]
    nums = regex.findall(filename)

    if nums:
        # "x * 10"的目的是为了让“20170201-2”也“20170202-1”不判断为相等
        return functools.reduce(lambda x, y: x * 10 + int(y), nums, 0)
    else:
        return filename


def sort_image_file_paths(image_file_paths, n=3):
    '''
    排序图片文件路径组成的序列

    @image_file_paths：需排序的图片文件路径组成的序列。
    @n: 几张图片为一组

    排序方法：
    1. 对于普通文件名，按字母顺序排序
    2. 对于"1[xX]2[.jpeg]"名称的文件名，“1”表示第1辆车，“2”表示第1辆车的第2张图片。

    如果对插入图片重命名有误，则返回消息字符串
    否则返回排序好的路径组成序列。
    '''

    # 正常名称路径组成的序列
    normal_paths = []
    # key为特殊路径名，value为以car_index和pic_index得出的在最后返回链表中的索引
    special_paths = dict()

    regex = re.compile(
        r'.*[^0-9](?P<car_index>\d+)[xX](?P<pic_index>[0-9]+)(?:.[jpeg|png|gif])?', re.IGNORECASE)

    for path in image_file_paths:
        mo = regex.match(path)
        if mo:
            car_index = int(mo.group('car_index'))
            pic_index = int(mo.group('pic_index'))
            # print(path, len(image_file_paths) / n,
            #       'car_index:', car_index, 'pic_index:', pic_index)

            if (car_index > len(image_file_paths) / n) or (pic_index > n) or (pic_index <= 0):
                return '{}：文件名有误，请重命名该文件'.format(path)

            special_paths[path] = (car_index - 1) * n + (pic_index - 1)
        else:
            normal_paths.append(path)

    # 排序正常名称图片路径
    normal_paths.sort(key=alphanum_key)

    # 如果不使用OrderedDict会造成插入混乱
    special_paths = OrderedDict(
        sorted(special_paths.items(), key=lambda x: x[1]))

    for path, index in special_paths.items():
        normal_paths.insert(index, path)

    return normal_paths
