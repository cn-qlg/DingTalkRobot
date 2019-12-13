# DingTalkRobot
钉钉推送机器人

由于项目[DingtalkChatbot](https://github.com/zhuifengshen/DingtalkChatbot) 作者不再维护，出于自用以及学习的目的，创建此项目。
[官方文档说明](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)。

### 主要功能：
1. 支持多种安全设置, 关键词以及加签方式
2. 支持text, link, mark_down等方式推送
3. 支持@指定人员
4. 支持@所有

### 使用方法:
#### 一、钉钉机器人设置
1. 下载钉钉电脑桌面版本。
2. 在需要引入机器人的群，右上角群设置，智能群助手->添加机器人->选择自定义机器人（选择其他类型机器人似乎也可以，未测试）。
3. 在新添加的机器人设置界面，可以看到Webhook，以及安全设置。
4. 安全设置中，选择你所需要的安全设置。如果选择加签模式，则可以获得对应的秘钥。
#### 二、代码引入
```
webhook = "webhook"
secret = "secret"
robot = DingTalkRobot(webhook, secret)
robot.send_text("重要通知")
robot.send_link(
        "重要通知", "钉钉官方文档", "https://ding-doc.dingtalk.comdoc#/serverapi2/qf2nxq")
mark_down = "#### 杭州天气" + \
    "> 9度，西北风1级，空气良89，相对温度73%\n\n" + \
    "> ![screenshot](https://gw.alicdn.com/tfsTB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)\n" + \
    "> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n"
robot.send_markdown("杭州天气", mark_down)
```