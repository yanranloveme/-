import smtplib
from email.mime.text import MIMEText

import Settings


# % 邮件部分 %
def send_email(subject, message):  # 发送一封邮件
    msg_from = Settings.email_address  # 发送方邮箱
    passwd = Settings.email_password  # 发送方邮箱密码
    msg_to = Settings.email_address  # 接收方，即自己给自己发
    subject = subject  # 主题
    msg = MIMEText(message)  # HTML纯文本格式发送邮件
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    s = smtplib.SMTP_SSL(Settings.email_server, Settings.email_port)  # 邮件服务器（逗号前）及端口号（逗号后）
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())