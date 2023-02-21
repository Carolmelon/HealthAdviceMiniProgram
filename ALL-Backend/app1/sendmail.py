import smtplib
from email.header import Header
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # SMTP服务器
mail_user = " "  # 用户名
mail_pass = " "  # 授权密码，非登录密码

sender = 'example@163.com'  # 发件人邮箱(最好写全, 不然会失败)
receivers = ['example@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
receiver = 'example@qq.com'

content = 'QQ邮箱请不要拦截'
title = '测试邮件'  # 邮件主题


def sendEmail():
    # message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message = MIMEText('<html><body><h1>提醒卓越壹生管理员</h1>' +
                       '<p>send by example' + '</p>' +
                       '<p>' + content + '</p>' +
                       '<a href="http://www.example.cn/">点击这里进入网站查看</a>' +
                       '</body></html>', 'html', 'utf-8')
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


def send_email2(content, manage_url='http://www.example.cn/', SMTP_host="smtp.163.com", from_account='example@163.com',
                from_passwd="example", to_account='example@qq.com', subject="卓越壹生网站有消息了"):
    #print("\nstart_send_email\n")
    email_client = smtplib.SMTP_SSL(SMTP_host, 465)
    #print("\nstart_send_email:1\n")
    email_client.login(from_account, from_passwd)
    #print("\nstart_send_email:2\n")
    # create msg
    msg = MIMEText('<html><body><h1>提醒卓越壹生管理员</h1>' +
                       '<p>send by example' + '</p>' +
                       '<div>' + content + '</div>' +
                       '<a href="' + manage_url + '">点击这里进入网站查看</a>' +
                       '</body></html>', 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = to_account
    email_client.sendmail(from_account, to_account, msg.as_string())
    # print("发送完了邮件")
    email_client.quit()

def send_email_async(content, manage_url='http://www.example.cn/', SMTP_host="smtp.163.com", from_account='example@163.com',
                from_passwd="example", to_account='example@qq.com', subject="卓越壹生网站有消息了"):
    import threading, time
    def send_email_without_error():
        # time.sleep(10) 模拟延迟
        try:
            send_email2(content,to_account=to_account,manage_url=manage_url)
        except:
            pass
    t = threading.Thread(target=send_email_without_error)
    t.start()
    



if __name__ == '__main__':
    print("发送前")
    # send_email2(mail_host, sender, mail_pass, receiver, title, content)
    sendEmail()
    print("发送后")

