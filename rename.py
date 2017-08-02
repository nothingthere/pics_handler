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
if not cpus:
    cpus = 1

MAX_WORKERS = 5 * cpus


def move_files(paths_from, paths_to, func=shutil.copy2):
    '''
    理由多线程复制/或重命名文件
    默认为复制文件，及使用shutil.copy2
    可使用os.rename实现重命名
    '''
    # def foo(x, y):
    #     func(x, y)
    #     print(os.path.basename(x), ' --> ', os.path.basename(y))

    # 传递max_workers参数是为了兼容python3.4，以兼容XP
    with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as e:
        e.map(func, paths_from, paths_to)


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
    fake_index = 999              # 如果是“将来”的图片
    car_index = 0

    pic_index = 1
    filepaths_in_dst_folder = public.filepaths_in_folder(dst_folder)

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
                fake_index += 1
                car_index = fake_index

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

    4. 如果duplicated_paths中有路径，则表明为当前文件夹中修改，
       1. 先将所有所有旧路径重命名为"新路径.new"即old_path1 -> new_path1.new
       2. 再将所有“新路径.new” 重命名为“新路径”，即new_path1.new -> new_path
          按照os.rename的机制，会覆盖之前duplicated_paths中的“新路径”
       3. 如果是添加照片组，则文件夹中的照片会变得“干净”。如果删减照片组，也会
         变得“干净”。

    5. 如果duplicated_paths中没有路径，则有可能是当前文件夹中修改，也有可能不是，
       此时使用inplace参数判断是否在当前文件夹中修改。
    '''

    # 1、2和3
    paths = generate_path_pairs(
        file2datetimes, dst_folder, edited, inplace=inplace)
    old_paths = paths[0]
    new_paths = paths[1]
    duplicated_paths = paths[2]
    flag = '.NEW'

    try:
        # 4
        if len(duplicated_paths) > 0:
            new_paths2 = []
            for path in new_paths:
                new_paths2.append(path + flag)

            move_files(old_paths, new_paths2, os.rename)
            move_files(new_paths2, new_paths, os.rename)
        # 5
        else:
            if inplace:
                # print('\t重命名')
                move_files(old_paths, new_paths, os.rename)
            else:
                # print('\t复制')
                move_files(old_paths, new_paths, shutil.copy2)

    except:
        return '''重命名图片失败，
        请查看是否有其他程序占用图片或图片所在文件夹
        '''

    return True
