# 晨午晚检填写程序
import json
import time

from EmailSender import send_email
from Verifi import conn

import MainFunc
import Settings


def up(subject):
    # % 数据部分 %
    data = {
        "ymtys": "0",  # 一码通颜色
        "sfzx": "1",  # 是否在校
        "tw": "2",  # 体温范围：36.5°C~36.9°C
        "area": bytes(Settings.province, 'utf-8') + b'\x20' + bytes(Settings.city, 'utf-8') + b'\x20' + bytes(
            Settings.area,
            'utf-8'),  # 省市区
        "city": bytes(Settings.city, 'utf-8'),  # 市
        "province": bytes(Settings.province, 'utf-8'),  # 省
        "address": bytes(Settings.address, 'utf-8'),  # 具体地点
        "sfcyglq": "0",  # 是否处于隔离期
        "sfyzz": "0",  # 是否出现乏力、干咳、呼吸困难等症状
        "qtqk": "",  # 其他情况
        "askforleave": "0"
    }

    result_main = conn.post(
        url="https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save",
        data=data  # 填写数据
    )

    # @ 错误2：数据发送错误 @
    if result_main.status_code != 200:
        print("数据发送错误，错误代码：", result_main.status_code)
        send_email(subject, MainFunc.BJT + '\n' + '数据发送错误，错误代码：' + result_main.status_code)
        exit()
    else:
        try:
            # @ 程序完成 @
            result_json = json.loads(result_main.text)
            print(MainFunc.BJT + '\n程序完成。\n' + str(result_json['e']) + '-' + result_json['m'])
            send_email(subject, MainFunc.BJT + '\n程序完成。\n' + str(result_json['e']) + '-' + result_json['m'])
        except json.decoder.JSONDecodeError:
            print('晨午晚检填报程序数据发送部分出现异常。请检查是否按照步骤进行配置。')
            send_email(subject, MainFunc.BJT + '晨午晚检填报程序数据发送部分出现异常。请检查是否按照步骤进行配置。')
