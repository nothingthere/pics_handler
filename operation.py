#!/usr/bin/python3
# operation.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-28 20:56:41
# Code:
'''
operation_frame操作函数
'''
import datetime
import excel
import exifread
import os.path
import public
import re
import rename
import validate
from tkinter import messagebox

# 元数据中照片创建时间格式固定。
# 参考地址：https://www.media.mit.edu/pia/Research/deepview/exif.html
# 格式为：2017:07:20 13:04:01
exif_date_regex = re.compile(r'''
(?P<year>\d{4}):(?P<month>\d{2}):(?P<day>\d{2})
[ ](?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})
''',
                             re.VERBOSE)


# 当有图片丢失时，添加图片命名方式为时间格式，
# 以伪造拍照时间，
# 格式为：2017-07-20-13-04-01
# 其中最后一个数字为1、2或3，用于指定在3张图片中的位置，
# 如果有少于3张照片丢失，伪造图片会拍在前面
fake_date_regex = re.compile(r'''
(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})
-(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<second>\d{2})
''',
                             re.VERBOSE)
# print(exif_date_regex.match('2017:07:29 00:13:58')

#
# 信息获取
#


def extract_from_image(image_file):
    '提取照片创建时间，返回元组：(文件路径:datetime键值对)'

    with open(image_file, 'rb') as fp:
        tags = exifread.process_file(fp, stop_tag='EXIF')
        timestring = tags.get('EXIF DateTimeOriginal').values

        if exif_date_regex.match(timestring):
            datetime_ = datetime.datetime.strptime(
                timestring, '%Y:%m:%d %H:%M:%S')
            return (image_file, datetime_)

    # None：用于验证是否可提取创建时间，
    # 实际操作过程中，由于验证过，所以不会有value为None
    return (image_file, None)


def extract_from_images(image_files):
    '''
    返回按创建时间排序好的 (图片路径, 创建时间)元组组成的序列
    '''
    files2datetime = []

    for image_file in image_files:
        pure_file_name = os.path.splitext(os.path.basename(image_file))[0]
        pair = list(extract_from_image(image_file))
        if fake_date_regex.match(pure_file_name):
            # print('伪造成功', pure_file_name)
            pair[1] = datetime.datetime.strptime(
                pure_file_name, '%Y-%m-%d-%H-%M-%S')

        files2datetime.append(tuple(pair))

    files2datetime.sort(key=lambda pair: pair[1])

    return files2datetime


def generate_car_datetimes(files2datetime):
    '''
    @files2datetime：extract_form_images的返回值

    返回“创建时间”元组组成的序列
    在files2datetime中每3个元素提取其中一个
    '''
    result = []

    for i in range(0, len(files2datetime), 3):
        result.append(files2datetime[i][1])

    return result


def get_not_edited(car_datetimes):
    '''获取昨天没编辑的车辆数
    '''
    not_edited = 0

    current_date = public.date_current()

    for datetime_ in car_datetimes:
        car_date = public.datetime2date(datetime_)

        if (current_date - car_date).days == 1:
            not_edited += 1

    return not_edited

#
# 总入口
#

# UI更新写在逻辑层是否有点不好


def update_progress(root, progress_str, message=''):
    if root and progress_str:
        progress_str.set(message)
        root.update_idletasks()


def main(default_lane=7, image_files={},
         src_folder='', dst_folder='', excel_file='',
         root=None, progress_str=None):
    '''
    总的执行函数，
    如果失败，返回消息字符串，否则返回True
    '''

    inplace = src_folder == dst_folder  # os.path.samefile在Win7_32中好像会出错
    inplace_OK = True

    if inplace:
        inplace_OK = messagebox.askyesno(
            title='警告',
            message='确定要在当前文件夹中修改？')

    if not inplace_OK:
        return '操作被取消'
    #
    # 提取所需数据
    #
    update_progress(root, progress_str, '正在获取文件信息...')
    # inplace = os.path.samefile(src_folder, dst_folder)

    file2datetimes = extract_from_images(image_files)
    car_datetimes = generate_car_datetimes(file2datetimes)

    # 此时才能判断是否可正确提取元数据
    can_extract_ctime = validate.image_file(file2datetimes[0][0])
    if isinstance(can_extract_ctime, str):
        update_progress(root, progress_str, '')
        return can_extract_ctime

    not_edited = get_not_edited(car_datetimes)
    edited_and_row_start = excel.get_edited_and_row_start(excel_file,
                                                          car_datetimes[0])
    edited = edited_and_row_start[0]
    row_start = edited_and_row_start[1]

    # for pair in file2datetimes:
    #     print(pair[0], '  -> ', pair[1])

    # print('''
    # inplace: {},
    # car_datetimes: {},
    # edited: {},
    # not_edited: {},
    # row_start: {},
    # '''.format(inplace,
    #            car_datetimes,
    #            edited, not_edited,
    #            row_start))
    # return True

    # 照片重命名
    #
    update_progress(root, progress_str, '正在重命名图片....')
    result = rename.main(file2datetimes, dst_folder,
                         edited=edited, inplace=inplace)
    if isinstance(result, str):
        update_progress(root, progress_str, '')
        return result

    # print('重命名照片结束')
    #
    # 操作excel文件
    #

    update_progress(root, progress_str, '正在写入Excel文件....')

    result = excel.main(excel_file, car_datetimes, row_start,
                        default_lane=default_lane,
                        edited=edited, not_edited=not_edited)
    if isinstance(result, str):
        update_progress(root, progress_str, '')
        return result

    update_progress(root, progress_str, '')

    return True
