# whu_gym
自动预约WHU体育场馆脚本，基于 zfb132 的 [gym_place_order](https://github.com/zfb132/gym_place_order) 进行改造，并增加Github Action支持


### 使用

1. 修改`config.py`中的参数

一些示例

```python
#卓尔体育馆10、羽毛球22、fdid:134起、下一天、19:30、20:30
res = submit_order(usr_id, 10, 22, 141, tomorrow+" 19:30:00", tomorrow+" 20:30:00")
        
# 风雨体育馆2、羽毛球4、fdId:27是一号场地
res = submit_order(usr_id, 2, 4, 28, tomorrow+" 19:30:00", tomorrow+" 20:30:00")

# 风雨体育馆2、乒乓球5、fdid:35是一号场地
res = submit_order(usr_id, 2, 5, 36, tomorrow+" 19:30:00", tomorrow+" 20:30:00")

```

2. 设置Secrets

将`config.py`注明的变量在repo的Setting->Secrets中一一设置

变量名和值默认都是字符串类型，不需要加引号（重点）

3. 安装环境

需要先安装`requests、twilio` 库，再运行`myreserve.py`

这一步骤使用Action自动化了

4. 定时运行

学校每天 **18:02:50** 开放第二天的预约，yml中默认这个点运行脚本

若想要立即执行等，请自行修改yml文件