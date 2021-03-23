import datetime
import time

import Settings
import DailyUp
import DailyReport

BJT = str(datetime.datetime.now() + datetime.timedelta(hours=+8))[:-7]  # 时间

if __name__ == '__main__':
    a = int(time.strftime("%H", time.localtime()))
    a = (a + 8) % 24
    if Settings.DailyUp and a <= 12:
        DailyUp.up('晨检')
    if Settings.DailyUp and 12 <= a < 18:
        DailyUp.up('午检')
    if Settings.DailyUp and a > 18:
        DailyUp.up('晚检')

    if Settings.DailyReport and a <= 10:
        DailyReport.report()
