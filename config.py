#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-08-26 10:13

# 预约场馆id
GGID = 2  # 风雨
# 预约场地分块id（该场馆这类运动的编号）
FFID = 4  # 羽毛球
# 场地id（所有场馆统一编号）
FDID = 28  # 二号场

# 预约日期：0表示当天；1表示下一天；2表示下下天
RESERVE_DATE = 2  # 明天
# 预约最早开始时间
RESERVE_START_TIME = "18:00:00"
# 预约最晚结束时间
RESERVE_END_TIME = "21:00:00"


'''
为了用户隐私，以下变量放到github secrets中
'''
# 体育馆预约系统的账户配置
GYM_USER = 'xxx'
GYM_PWD = 'xxx'


# twilio发信账户配置
SMS_SID = 'xxx'
SMS_TOKEN = 'xxx'
SMS_FROM_NUMBER = 'xxx'  # 带区号

# 接收短信通知的手机号
SMS_TO_NUMBER = 'xxx'  # 带区号

# 邮箱发信账户配置
EMAIL_FROM = 'xxx@qq.com'
EMAIL_PWD = 'xxx'  # 用的SMTP授权码，而不是密码
EMAIL_TO = 'xxx@qq.com'
