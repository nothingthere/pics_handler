#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-14 23:15:46
# Code:
'''
utils.py测试脚本
'''

import functools
import os
import os.path
import re
import shutil
import utils

IMAGE_FOLDER = '/home/claudio/Desktop/Python/pics-handler/test_pics'
NEW_IMAGE_FOLDER = IMAGE_FOLDER + '.NEW'

images = os.listdir(IMAGE_FOLDER)
new_images = os.listdir(NEW_IMAGE_FOLDER)

IMAGES = []
for i in images:
    IMAGES.append(os.path.join(IMAGE_FOLDER, i))

# print(IMAGES)
NEW_IMAGES = []
for i in new_images:
    NEW_IMAGES.append(os.path.join(NEW_IMAGE_FOLDER, i))
# for i in NEW_IMAGES:
#     print(i)

#
# validate_num_input
#

assert utils.validate_num_input('0') == 0
assert utils.validate_num_input('  ') == 0
assert utils.validate_num_input('  01  ') == 1
assert isinstance(utils.validate_num_input(' 1x '), str)

#
# validate_images_folder
#


print('测试对输入内容转换为整数是否正确')
assert '请选择文件夹先' == utils.validate_images_folder('')
assert '不存在此文件夹' in utils.validate_images_folder('foo/bar')
assert '不为文件夹' in utils.validate_images_folder(IMAGES[0])

print('测试对文件夹的验证')
temp_name = IMAGES[0].strip('JPG')
os.rename(IMAGES[0], temp_name)
assert '整数倍' in utils.validate_images_folder(IMAGE_FOLDER)
os.rename(temp_name, IMAGES[0])

assert utils.validate_images_folder(IMAGE_FOLDER) == IMAGES

#
# sort_image_file_paths
#
print('测试排序是否正确')
sorted_images = utils.sort_image_file_paths(IMAGES)
for i in sorted_images:
    print(i)
assert '2x2' in sorted_images[4].lower()
assert '12x03' in sorted_images[35].lower()
assert '10x3' in sorted_images[29].lower()

#
# construct_new_names
#
new_names = utils.construct_new_names(IMAGES, NEW_IMAGE_FOLDER)

print('测试命名是否正确')
regex = re.compile(r'\d{8}\d{3}-\d{1}')

for old, new in zip(IMAGES, new_names):
    mo = regex.search(new)
    assert mo is not None
    # print(new)

new_names = utils.construct_new_names(NEW_IMAGES, NEW_IMAGE_FOLDER)
for new in new_names:
    mo = regex.search(new)
    assert mo is not None
    mo = regex.search(new)
    assert mo is not None


#
# move_files
#


print('不在当前文件夹中修改')
shutil.rmtree(NEW_IMAGE_FOLDER)
os.mkdir(NEW_IMAGE_FOLDER)
old_names = IMAGES
new_names = utils.construct_new_names(old_names, NEW_IMAGE_FOLDER)


utils.move_files(utils.sort_image_file_paths(old_names), new_names)

first_flaged_file = '2x2'
second_flaged_file = '10x3'
third_flaged_file = '12x03'

for image in IMAGES:
    if first_flaged_file in image.lower():
        first_flaged_file = image
    if second_flaged_file in image.lower():
        second_flaged_file = image
    if third_flaged_file in image.lower():
        third_flaged_file = image


assert os.stat(first_flaged_file).st_size == os.stat(new_names[4]).st_size
assert os.stat(second_flaged_file).st_size == os.stat(new_names[29]).st_size
assert os.stat(third_flaged_file).st_size == os.stat(new_names[35]).st_size

print('在当前文件夹中修改')
# print('\t重命名')
new_names = utils.construct_new_names(NEW_IMAGES, NEW_IMAGE_FOLDER, skip=0)
# for name in new_names:
#     assert name.endswith('_new')

utils.move_files(utils.sort_image_file_paths(NEW_IMAGES), new_names)
utils.move_files(new_names, utils.construct_resolution_new_names(
    new_names), func=os.rename)

#
# 成功
#
print('\n\t测试通过')
