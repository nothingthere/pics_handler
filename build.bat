REM Author: Claudio <3261958605@qq.com>
REM Created: 2017-07-13 21:48:14
REM Commentary:
REM Code:
pyinstaller --noconfirm ^
            --noconsole ^
            --clean ^
            --add-data="sdgs.png;." ^
            --add-data="sdgs.ico;." ^
            --add-data="folder.png;." ^
            --add-data="excel.png;." ^
            -i banana.ico ^
            --name="pics_handler0.3.3.1" ^
            pics_handler.py


