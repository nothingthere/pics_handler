#!/bin/bash
# 编译命令
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-13 21:48:14
# Commentary:
# Code:
pyinstaller --noconfirm \
            --onefile \
            --nowindowed \
            --clean \
            --icon logo.png \
            app.py

exit
