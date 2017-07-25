REM Author: Claudio <3261958605@qq.com>
REM Created: 2017-07-13 21:48:14
REM Commentary:
REM Code:
pyinstaller --noconfirm ^
            --noconsole ^
            --clean ^
            --add-data="sdgs.gif;." ^
            --add-data="sdgs.ico;." ^
            -i baicai.ico ^
            app.py

