import datetime
import time
from reserve import send_email, send_sms
import os


now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(now)

SMS_SID = os.environ['SMS_SID']
SMS_TOKEN = os.environ['SMS_TOKEN']
SMS_FROM_NUMBER = os.environ['SMS_FROM_NUMBER']
SMS_TO_NUMBER = os.environ['SMS_TO_NUMBER']

print(type(SMS_FROM_NUMBER))
print(SMS_FROM_NUMBER[:-1])
print(SMS_FROM_NUMBER[:])
print(SMS_SID[:-1])
send_sms(SMS_TO_NUMBER, "你好，测试")

