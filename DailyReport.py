# 疫情通填写程序
import smtplib
import json
from email.mime.text import MIMEText

from EmailSender import send_email
from Verifi import conn

import MainFunc
import Settings


def report():
    # % 数据部分 %
    data = {
        "sfzx": "1",  # 是否在校：否0是1
        "sfzgn": "1",  # 所在地点：中国大陆为1
        "area": bytes(Settings.province, 'utf-8') + b'\x20' + bytes(Settings.city, 'utf-8') + b'\x20' + bytes(
            Settings.area,
            'utf-8'),  # 省市区
        "city": bytes(Settings.city, 'utf-8'),  # 市
        "province": bytes(Settings.province, 'utf-8'),  # 省
        "address": bytes(Settings.address, 'utf-8'),  # 具体地点
        "zgfxdq": "0",  # 是否在中高风险地区：否0是1
        "tw": "3",  # 体温范围：36.5°C~36.9°C
        "sfcxtz": "0",  # 是否出现症状：否0是1
        "sfjcbh": "0",  # 是否接触接触无症状感染/疑似/确诊人群：否0是1
        "mjry": "0",  # 是否接触密接人员：否0是1
        "csmjry": "0",  # 是否去过疫情场所：否0是1
        "sfcyglq": "0",  # 是否处于隔离期：否0是1
        "sfjcjwry": "0",  # 是否接触境外人员：否0是1
        "sfcxzysx": "0",  # 是否有特别情况：否0是1
        "multiText": "",  # 其他情况
    }

    result_main = conn.post(
        url="https://xxcapp.xidian.edu.cn/ncov/wap/default/save",
        data=data  # 填写数据
    )

    # @ 错误2：数据发送错误 @
    if result_main.status_code != 200:
        print("数据发送错误，错误代码：", result_main.status_code)
        send_email('疫情通', MainFunc.BJT + '\n' + '数据发送错误，错误代码：' + result_main.status_code)
        exit()
    else:
        try:
            # @ 程序完成 @
            result_json = json.loads(result_main.text)
            print(MainFunc.BJT + '\n程序完成。\n' + str(result_json['e']) + '-' + result_json['m'])
            send_email('疫情通', MainFunc.BJT + '\n程序完成。\n' + str(result_json['e']) + '-' + result_json['m'])
        except json.decoder.JSONDecodeError:
            print('疫情通填报程序数据发送部分出现异常。请检查是否按照步骤进行配置。')
            send_email('疫情通', MainFunc.BJT + '疫情通填报程序数据发送部分出现异常。请检查是否按照步骤进行配置。')
