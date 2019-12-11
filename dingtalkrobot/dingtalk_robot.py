import requests
import time

def is_null_or_blank_str(content):
    """是否为空字符串"""
    if not content or not content.strip():
        return True
    return False


class DingTalkRobot(object):
    """钉钉自定义机器人"""

    def __init__(self, webhook, secret_key):
        self.webhook = webhook
        self.secret_key = secret_key    

    def send_text(self, msg, is_at_all=False, at_mobiles=None):
        if is_null_or_blank_str(msg):
            raise ValueError("Text类型，msg不能为空！")
        post_data = {"msgtype": "text", "at": {}}

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
        pass
