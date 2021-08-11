#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-08-21 18:12
import datetime
import json
import requests
import sys
import time

import config
import os

# 获取环境变量
GYM_USER = os.environ['GYM_USER']
GYM_PWD = os.environ['GYM_PWD']

SMS_SID = os.environ['SMS_SID']
SMS_TOKEN = os.environ['SMS_TOKEN']
SMS_FROM_NUMBER = os.environ['SMS_FROM_NUMBER']
SMS_TO_NUMBER = os.environ['SMS_TO_NUMBER']

EMAIL_FROM = os.environ['EMAIL_FROM']
EMAIL_PWD = os.environ['EMAIL_PWD']
EMAIL_TO = os.environ['EMAIL_TO']


# 使用邮箱发送通知功能
def send_email(email, subject, msg):
    from smtplib import SMTPException, SMTP_SSL
    from email.mime.text import MIMEText
    from email.header import Header
    sender = EMAIL_FROM
    pwd = EMAIL_PWD
    # 三个参数：第一个为文本内容，第二个为plain设置文本格式，第三个为utf-8设置编码
    message = MIMEText(msg,"plain",'utf-8')
    message ['From'] = Header(sender,'utf-8')
    message ['To'] = Header(email,'utf-8')
    message["Subject"] = Header(subject,"utf-8")
    try:
        # 使用非本地服务器，需要建立ssl连接
        smtpObj = SMTP_SSL("smtp.qq.com",465)
        smtpObj.login(sender,pwd)
        smtpObj.sendmail(sender,email,message.as_string())
        print("邮件发送成功")
    except SMTPException as e:
        print("Error：无法发送邮件.Case:%s"%e)


# 使用twilio的使用账户发送短信
def send_sms(phone, content):
    from twilio.rest import Client
    # 账户信息： twilio.com/console
    account_sid = SMS_SID
    auth_token = SMS_TOKEN
    from_phone_num = SMS_FROM_NUMBER
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=content, from_=from_phone_num, to=phone)
    # print(message.sid)
    print("短信发送成功")


# 报头
header = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 ",
    'Host':"gym.whu.edu.cn"
}
URL_BASE = "http://gym.whu.edu.cn:80/"


# 登录系统，获取cookies
def login(user_name, user_pwd):
    url = URL_BASE + "loginAction!UserLogin"
    login_params = {
        "name":user_name,
        "password":user_pwd
    }
    result = requests.post(url=url, headers=header, data=login_params)
    print('提交登录：'+result.text)
    status = json.loads(result.text)['status']
    if(status == -1):
        # 登陆成功，返回cookies
        return result.cookies
    else:
        return ""


# 返回个人信息list
# 昵称、未知、身份、邮箱、学校、电话、生日、rlId、ssId、upId
def get_user_info(cookies):
    url = URL_BASE + "UserAction!getUserInfoToMobile"
    cookie = "JSESSIONID={}".format(cookies.get("JSESSIONID"))
    header["cookie"] = cookie
    result = requests.post(url=url, headers=header)
    print('个人信息：'+result.text)
    return json.loads(result.text)


# 提交订单
# ggId表示体育馆id，ffId是场地分块id（该场馆各类运动统一编号）、fdId是场地id（所有场馆统一编号）
def submit_order(usrId, ggId, ffId, fdId, start_time, end_time):
    url = URL_BASE + "OrderAction!bookOrder?deposit=0.00"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_params = {
        "ggId": ggId,
        "ffId": ffId,
        "fdId": fdId,
        "usrId": usrId,
        "beginTime": start_time,
        "endTime": end_time,
        "ordTime": now,
        "payType": 2
    }
    result = requests.post(url=url, headers=header, data=order_params)
    print('当前时间：'+now)
    print('预约结果：'+result.text)
    # -1是被预约了，-5是下一天的还没有更新
    if (result.text == "-1") or (result.text == "-5"):
        print("预约失败")
        return False
    else:
        print("预约成功")
        content = "{}元；{}；{}--{}".format(
            json.loads(result.text)["money"], start_time[0:10], start_time[-8:-3], end_time[-8:-3]
        )
        send_email(EMAIL_TO, '体育馆预约', content)
        send_sms(SMS_TO_NUMBER, content)
        return True


if __name__ == "__main__":
    # 提取保持登录
    cookies = login(GYM_USER, GYM_PWD)
    usr_id = int(get_user_info(cookies)[-1]) + 5
    tomorrow = (datetime.date.today() + datetime.timedelta(days=config.RESERVE_DATE)).strftime("%Y-%m-%d")
    
    
    # 延时
    while True:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        print(hour, minute, second)
        if hour == 10 and minute == 1 and second <= 47:
            time.sleep(1)
            print("sleep 1")
        else:
            break

    # time.sleep(48)  # 18:01:50 提前2秒抢


    res = False
    cnt = 10  # 持续10轮

    while((res == False) and (cnt > 0)):
        for fdid in range(27, 27+6):
            res = submit_order(usr_id, config.GGID, config.FFID, config.FDID, tomorrow+config.RESERVE_START_TIME, tomorrow+config.RESERVE_END_TIME)
            # res = submit_order(usr_id, 2, 5, 36, tomorrow+" 19:30:00", tomorrow+" 20:30:00")
            time.sleep(0.1)
            if res == True:
                break
        cnt -= 1

    print("")
