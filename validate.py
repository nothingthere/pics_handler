#!/usr/bin/python3
# validate.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-28 21:24:41
# Code:
'''
验证获取内容
'''


import operation
import os
import os.path
import public
import shutil
import tkinter.messagebox as messagebox


def show_error(message, widget=None):
    '''
    操作错误提示

    @widget：如果出现操作错误时，需focus的元素
    '''
    messagebox.showerror(title='错误', message=message)
    if widget:
        widget.focus()


def str2num(string):
    string = string.strip()
    try:
        if '' == string:
            return 0
        return int(string)
    except ValueError:
        return None


# def edited(tk_str, focus):
#     result = str2num(tk_str.get())

#     if None is result:
#         show_error('请使用纯数字设置车辆数', focus)
#         return False

#     return result


def default_lane(tk_str, focus):
    result = str2num(tk_str.get())

    if None is result:
        show_error('请使用纯数字设置鲜活车常过车道', focus)
        return False

    return result


def src_folder(tk_str, focus):
    folder_path = tk_str.get().strip()
    image_files = []

    pics_per_car = 3

    if '' == folder_path:
        show_error('请选择待处理照片所在文件夹', focus)
        return False

    if not os.path.exists(folder_path):
        show_error('{}：不存在此文件夹'.format(folder_path),
                   focus)
        return False

    if not os.path.isdir(folder_path):
        show_error('{}：不为文件夹'.format(folder_path),
                   focus)
        return False

    for filepath in public.filepaths_in_folder(folder_path):
        extension = os.path.splitext(filepath)[1]
        if extension.lower() in public.IMAGE_FILE_EXTENSIONS:
            image_files.append(filepath)

    if 0 == len(image_files):
        show_error('{}：无图片文件'.format(folder_path))
        return False

    if 0 != len(image_files) % pics_per_car:
        show_error('{}：图片文件不为3的整数倍'.format(folder_path))
        return False

    return image_files


def clear_folder(folder):
    '清空文件夹中第一层的图片文件'
    for filepath in public.filepaths_in_folder(folder):
        extention = os.path.splitext(filepath)[1]
        if extention.lower() in public.IMAGE_FILE_EXTENSIONS:
            os.remove(filepath)


def dst_folder(tk_str, src_folder, focus):
    folder_path = tk_str.get().strip()

    if '' == folder_path:
        show_error('请选择照片处理后放置文件夹', focus)
        return False

    if not os.path.exists(folder_path):
        show_error('{}：不存在此文件夹'.format(folder_path),
                   focus)
        return False

    if not os.path.isdir(folder_path):
        show_error('{}：不为文件夹'.format(folder_path),
                   focus)
        return False

    # 如果不在当前文件夹中修改，目标文件夹中有文件，先确定是否清空图片文件
    # 不使用os.samefile：Windows中相同路径会判断失败？？？
    if folder_path != src_folder and len(os.listdir(folder_path)) > 0:
        empty_OK = messagebox.askyesno(
            title='提示',
            message='需先清空{}中的图片文件，是否继续？'.format(folder_path))
        if not empty_OK:
            return False

        try:
            clear_folder(folder_path)
        except:
            show_error('{}：可能被另一个程序占用，清空失败'.format(folder_path))
            return False

    # return False
    return folder_path


def excel_file(tk_str, focus):
    file_path = tk_str.get().strip()

    if '' == file_path:
        show_error('请选择需操作的excel文件', focus)
        return False

    if not os.path.exists(file_path):
        show_error('{}：不存在此文件'.format(file_path))
        return False

    if '.xlsx' != os.path.splitext(file_path)[1]:
        show_error('{}：不为xlsx文件'.format(file_path))
        return False

    return file_path


def image_file(filename):
    '验证是否可提取拍照时间.'
    date_now = public.date_current()
    image_piar = operation.extract_from_image(filename)

    if not image_piar[1]:
        return '不能提取照片拍照时间，请设置相机以记录拍照时间'

    date_image = public.datetime2date(image_piar[1])
    # print(date_now, date_image, (date_now - date_image).days)
    if (date_now - date_image).days > 1:
        return '{}：拍摄时间至少在2天前，不能处理'.format(image_piar[0])

    return True
