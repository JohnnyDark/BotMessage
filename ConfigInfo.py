import json
import os
import yaml

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def config_info():
    """读取yaml文档"""
    with open(CURRENT_PATH + "/new_config", encoding='utf-8') as conf:
        temp = yaml.load(conf.read())
        return temp


def message_info():
    """读取完整消息类型的json文档，message.json"""
    with open(CURRENT_PATH + "/message.json", encoding='utf-8') as conf:
        temp = json.load(conf)
        return temp["message_type"]


def content_info():
    """读取只包含消息内容的json文档，content.json"""
    with open(CURRENT_PATH + "/content.json", encoding='utf-8') as conf:
        temp = json.load(conf)
        # print(temp)
        return temp["content"]


if __name__ == '__main__':
    print(content_info())
