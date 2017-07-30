#!/usr/bin/python3
# rename.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-29 19:09:57
# Code:
'''
照片重命名脚本
'''
import concurrent.futures as cf
import datetime
import os
import os.path
import public
import shutil

cpus = os.cpu_count()
if cpus:
    MAX_WORKER = 5 * cpus
else:
    MAX_WORKER = 5


def move_files(paths_from, paths_to, func=shutil.copy2):
    '''
    理由多线程复制/或重命名文件
    默认为复制文件，及使用shutil.copy2
    可使用shutil.move实现重命名
    '''
    # def foo(x, y):
    #     func(x, y)
    #     print(x, ' --> ', y)

    # 传递max_workers参数是为了兼容python3.4，以兼容XP
    with cf.ThreadPoolExecutor(max_workers=MAX_WORKER) as e:
        e.map(func, paths_from, paths_to)


def remove_files(paths):
    # def foo(path):
    #     os.remove(path)
    #     print('删除：', path)
    with cf.ThreadPoolExecutor(max_workers=MAX_WORKER) as e:
        e.map(os.remove, paths)


def filepaths_in_folder(folder):
    filenames_in_folder = os.listdir(path=folder)
    filepaths_in_folder = []
    for filename in filenames_in_folder:
        filepaths_in_folder.append(os.path.join(folder, filename))

    return filepaths_in_folder


def generate_path_pairs(file2datetimes, dst_folder, edited=0, inplace=True):
    '''
    返回值：元组(old_paths, new_paths, duplicated_paths)

    @files2datetimes: [(路径名, 创建日期), ....]序列
    @dst_dir：目标文件夹
    @edited：昨天编辑好的车辆数
    '''
    pics_per_car = 3
    old_paths = []
    new_paths = []
    duplicated_paths = []
    date_current = public.date_current()
    car_index_today = 0
    car_index_yesterday = edited
    car_index = 'X'
    pic_index = 1
    filepaths_in_dst_folder = filepaths_in_folder(dst_folder)

    for i, pair in enumerate(file2datetimes):
        path = pair[0]
        extension = os.path.splitext(path)[1]
        folder = os.path.dirname(path)
        datetime_car = pair[1]
        year = datetime_car.year
        month = datetime_car.month
        day = datetime_car.day
        date_car = datetime.datetime(year=year, month=month, day=day)

        # 计算车辆索引
        if i % pics_per_car == 0:
            days = (date_current - date_car).days
            if 1 == days:
                car_index_yesterday += 1
                car_index = car_index_yesterday
            elif 0 == days:
                car_index_today += 1
                car_index = car_index_today
            else:
                car_index = 'X'

        # 计算照片索引
        pic_index = (i % pics_per_car) + 1
        # 构建路径对
        # print(year, month, day, car_index, pic_index)

        pic_name = '{}{:02}{:02}{:03}-{}'.format(
            year, month, day, car_index, pic_index)

        if inplace:
            new_path = os.path.join(folder, pic_name + extension)
        else:
            new_path = os.path.join(dst_folder, pic_name + extension)

        # 向old_path、new_paths和duplicated_paths中添加数据
        old_paths.append(path)
        new_paths.append(new_path)

        if new_path in filepaths_in_dst_folder:
            # print('重复')
            duplicated_paths.append(new_path)

    return (old_paths, new_paths, duplicated_paths)


def main(file2datetimes, dst_folder, edited=0, inplace=True):
    '''
    @files2datetime：元组(图片路径, datetime)组成的序列
    @dst_folder：处理后放置图片的文件夹
    @edited：昨天编辑好的车辆数
    @inplace：是否修改当前文件夹

    基本算法：
    1. 计算旧路径径组成的序列[旧路径1, 旧路径2, ...]：old_paths
    2. 计算新路径组成的序列[新路径1, 新路径2,...]:new_paths
    3. 如果新路径已经存在于目标文件夹中：
       生产序列[新路径1,新路径2...]：duplicated_paths

    4. 将duplicated_paths_中的“新路径”重命名为“新路径.back”
    5. 复制/重命名old_paths中的路径待new_paths对应位置的新路径：旧路径 -> 新路径
    6. 删除duplicated_paths中的所有“新路径.back”文件


    ？？？好像没有必要管理重复名称的照片！！！！
    '''

    # 1、2和3
    paths = generate_path_pairs(
        file2datetimes, dst_folder, edited, inplace=inplace)
    old_paths = paths[0]
    new_paths = paths[1]
    # duplicated_paths = paths[2]
    # duplicated_paths_back = []
    # flag = '.BACK'
    # for path in duplicated_paths:
    #     duplicated_paths_back.append(path + flag)

    try:
        # # 4
        # print('重命名重复文件')
        # move_files(duplicated_paths, duplicated_paths_back, shutil.copy2)

        # 5
        # print('复制/重命名')
        if inplace:
            # print('\t重命名')
            move_files(old_paths, new_paths, shutil.move)
        else:
            # print('\t复制')
            move_files(old_paths, new_paths, shutil.copy2)

        # # 6
        # print('删除重复文件')
        # remove_files(duplicated_paths_back)

    except:
        return '''重命名图片失败，
        请查看是否有其他程序占用图片或图片所在文件夹
        '''

    return True
