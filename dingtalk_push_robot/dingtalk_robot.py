import base64
import hmac
import json
import time
from hashlib import sha256

import requests


def is_null_or_blank_str(content):
    """是否为空字符串"""
    if not content or not content.strip():
        return True
    return False


_ALWAYS_SAFE = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                         b'abcdefghijklmnopqrstuvwxyz'
                         b'0123456789'
                         b'_.-~')


def get_hmac_sha256_sign(secret_key, data):
    key = secret_key.encode("utf-8")
    secret_enc = data.encode("utf-8")
    value = hmac.new(key, secret_enc, digestmod=sha256).digest()
    signature = base64.b64encode(value)
    return signature


def quote_bytes(bts):
    """like urllib.parse.quote(), but return the lowercase."""
    return ''.join([chr(char) if char in _ALWAYS_SAFE else '%{:02x}'.format(
        char) for char in bts])


class DingTalkPushRobot(object):
    """钉钉自定义机器人"""

    def __init__(self, web_hook, secret_key):
        self.web_hook = web_hook
        self.secret_key = secret_key
        self.times = 0

    def send_text(self, msg, is_at_all=False, at_mobiles=None):
        """推送text类型消息。          
        :param msg: 消息内容
        :param is_at_all: 是否@所有，可选 
        :param at_mobiles: 被@人的手机号，可选
        :return: 是否发送成功
        :rtype: bool
        """
        if is_null_or_blank_str(msg):
            raise ValueError("Text类型，msg不能为空！")
        post_data = {"msgtype": "text", "at": {}, "text": {"content": msg}}
        if is_at_all:
            post_data["at"]["isAtAll"] = is_at_all

        if at_mobiles:
            at_mobiles = list(map(str, at_mobiles))
            post_data["at"]["atMobiles"] = at_mobiles

        return self._post_msg(post_data)

    def send_link(self, title, text, msg_url, pic_url=None):
        """推送link类型消息。          
        :param title: 标题。
        :param text: 消息内容。 
        :param msg_url: 链接地址。
        :param pic_url: 配图图片地址，可选。
        :return: 是否发送成功
        :rtype: bool
        """
        if is_null_or_blank_str(title) or is_null_or_blank_str(text) or is_null_or_blank_str(msg_url):
            raise ValueError("Link类型，title、text、msg_url不能为空！")
        post_data = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": pic_url,
                "messageUrl": msg_url
            }
        }
        return self._post_msg(post_data)

    def send_markdown(self, title, text, is_at_all=False, at_mobiles=None):
        """推送markdown类型消息。          
        :param title: 标题。
        :param text: 消息内容。 
        :param is_at_all: 是否@所有，可选 
        :param at_mobiles: 被@人的手机号，可选
        :return: 是否发送成功
        :rtype: bool
        """
        if is_null_or_blank_str(title) or is_null_or_blank_str(text):
            raise ValueError("MarkDown类型，title、text不能为空！")
        post_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {}
        }
        if is_at_all:
            post_data["at"]["isAtAll"] = is_at_all

        if at_mobiles:
            at_mobiles = list(map(str, at_mobiles))
            post_data["at"]["atMobiles"] = at_mobiles

        return self._post_msg(post_data)

    def _post_msg(self, post_data):
        self.times += 1
        if self.times == 1:
            self.start_time = time.time()
        elif self.times % 20 == 0:
            if time.time() - self.start_time < 60:
                time.sleep(60)
            self.start_time = time.time()

        timestamp = int(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.secret_key}"
        sign = quote_bytes(get_hmac_sha256_sign(
            self.secret_key, string_to_sign))
        url = f"{self.web_hook}&timestamp={timestamp}&sign={sign}"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = json.dumps(post_data)
        print(requests.post(url, data, headers=headers).text)


if __name__ == "__main__":
    webhook = "webhook"
    secret = "secret"
    robot = DingTalkPushRobot(webhook, secret)
    robot.send_text("重要通知")
    robot.send_link(
        "重要通知", "钉钉官方文档", "https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq")
    mark_down = "#### 杭州天气" + \
                "> 9度，西北风1级，空气良89，相对温度73%\n\n" + \
                "> ![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)\n" + \
                "> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n"
    robot.send_markdown("杭州天气", mark_down)
