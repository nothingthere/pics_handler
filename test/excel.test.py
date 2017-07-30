#!/usr/bin/python3
# excel.test.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-26 09:45:04
# Code:
'''
excel.py测试脚本
'''
import datetime
import excel
import os
import os.path
import time

FILE = 'test.xlsx'
FILE2 = 'test2.xlsx'

test_file1 = 'a.txt'
test_file2 = 'b.txt'
test_file3 = 'c.txt'
test_files = [test_file1, test_file2, test_file3]


def create_file(name):
    with open(name, 'w'):
        pass


for file in test_files:
    create_file(file)


DATA = []
for file in test_files:
    DATA.append({'time': os.stat(file).st_ctime, 'lane': '7'})
print(DATA)

NOW_STRING = excel._stat_time_to_string(time.time())
NOW = time.time()


def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def test_get_sheet():
    sheet = excel.get_sheet(book)
    name = '{}月'.format(datetime.date.today().month)
    assert sheet
    assert name in book.get_sheet_names()
    assert sheet.cell(row=1, column=1).value == excel.HEADER['title']
    assert sheet.cell(row=2, column=1).value == excel.HEADER['company']
    headers = excel.HEADER['headers']
    for i in range(len(headers)):
        assert sheet.cell(row=3, column=i + 1).value == headers[i]

    print("\t\t创建sheet成功，且头信息正确")
    book.save(FILE)
    return sheet


def test_get_start_row(edited):
    row_start = excel.get_start_row(sheet, edited)
    assert row_start == len(excel.HEADER) + 1
    print("\t\t获取开始添加行正确")


remove_file(FILE)
remove_file(FILE2)
print("测试获取book...")

book = excel._load_book(FILE)
assert book
print("\t文件不存在时创建并获取成功")
book = excel._load_book(FILE)
print("\t存在时直接获取成功")
assert book


print("测试获取sheet...")
print("\t本来不存在时")
sheet = test_get_sheet()
print('\t文件本来存在时')
sheet = test_get_sheet()


print("将现在时间，作为时间戳格式化的结果为：")
print("\t{} {}".format(*NOW_STRING))


print("获取开始写入数据的信息...")
print("\t没有添加任何内容前")
test_get_start_row(0)


print("测试添加行...")
excel.add_entries(sheet, DATA, 0, 0)


def fake_data_test(edited, not_edited):
    print("\t在生产文件中伪造一个昨天车辆信息")
    row_start = len(excel.HEADER) + len(DATA)
    today = datetime.datetime.fromtimestamp(time.time())
    value = '{}.{:02}.{:02}'.format(today.year,
                                    today.month, today.day - 1)
    sheet.cell(row=row_start, column=2, value=value)
    print("\t再插入")
    # assert row_start + edited == excel.get_start_row(sheet, edited)
    # assert row_start == excel.get_start_row(sheet, edited)

    print("\t获取再次插入行正确")
    excel.add_entries(sheet, DATA, edited, not_edited)


# fake_data_test(0, 1)


fake_data_test(0, 3)
book.save(FILE2)


print("\n\n删除所有测试文件")
for file in [test_file1, test_file2, test_file3]:
    remove_file(file)

remove_file(FILE)

# remove_file(FILE2)
print("测试通过")
