import requests
import time
import hmac
from hashlib import sha256
import base64
from urllib import parse
import json


def is_null_or_blank_str(content):
    """是否为空字符串"""
    if not content or not content.strip():
        return True
    return False


def get_hmac_sha256_sign(secret_key, data):
    key = secret_key.encode("utf-8")
    secret_enc = data.encode("utf-8")
    value = hmac.new(key, secret_enc, digestmod=sha256).digest()
    print(value)
    signature = base64.b64encode(value)
    return signature


class DingTalkRobot(object):
    """钉钉自定义机器人"""

    def __init__(self, webhook, secret_key):
        self.webhook = webhook
        self.secret_key = secret_key
        self.times = 0

    def send_text(self, msg, is_at_all=False, at_mobiles=None):
        if is_null_or_blank_str(msg):
            raise ValueError("Text类型，msg不能为空！")
        post_data = {"msgtype": "text", "at": {}}
        post_data["text"] = msg
        if is_at_all:
            post_data["at"]["isAtAll"] = is_at_all

        if at_mobiles:
            at_mobiles = list(map(str, at_mobiles))
            post_data["at"]["atMobiles"] = at_mobiles

        return self._post_msg(post_data)

    def send_link(self, title, text, msg_url, pic_url=None):
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
        sign = parse.quote_plus(get_hmac_sha256_sign(
            self.secret_key, string_to_sign))
        url = f"{self.webhook}&timestamp={timestamp}&sign={sign}"
        print(url)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        print(requests.post(url, json.dumps(post_data), headers=headers).text)


if __name__ == "__main__":
    webhook = "webhook"
    secret = "secret"
    robot = DingTalkRobot(webhook, secret)
    robot.send_text("重要通知")
