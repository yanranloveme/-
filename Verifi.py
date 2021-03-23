# % 学生认证部分 %
import datetime
import json
import requests

import Settings
from EmailSender import send_email

BJT = str(datetime.datetime.now() + datetime.timedelta(hours=+8))[:-7]  # 时间
try:
    conn = requests.Session()
    result_login = conn.post(
        url='https://xxcapp.xidian.edu.cn/uc/wap/login/check',
        # username 学号，password 统一登录密码
        data={'username': Settings.stu_no, 'password': Settings.stu_pass}
    )
    login_json = json.loads(result_login.text)
    print(login_json['m'])
except requests.exceptions.ConnectionError:
    print("网络连接中断，请检查网络连接。")
    exit()

# @ 错误1：登录错误 @
if result_login.status_code != 200:
    print('登录连接错误，HTTP状态码：', result_login.status_code)
    send_email('登录错误', BJT + '\n' + '登录连接错误，HTTP状态码：' + result_login.status_code)
    exit()
else:
    try:
        if login_json['e'] != 0:
            print('登录错误，错误信息：' + str(login_json['e']) + '-' + login_json['m'])
            send_email('登录错误', BJT + '\n' + '登录错误，错误信息：' + str(login_json['e']) + '-' + login_json['m'])
            exit()
        else:
            print('登录成功。')
    except json.decoder.JSONDecodeError:
        print('疫情通及晨午晚检填报程序登录部分出现异常。请检查是否按照步骤进行配置。')
        send_email('填报程序出现异常', BJT + '疫情通及晨午晚检填报程序登录部分出现异常。请检查是否按照步骤进行配置。')
        exit()
