import datetime
import time
from reserve import send_sms
import os


now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(now)

SMS_TO_NUMBER = os.environ['SMS_TO_NUMBER']
send_sms(SMS_TO_NUMBER, "你好，测试")
