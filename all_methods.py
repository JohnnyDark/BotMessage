import json
import random

import requests

from ConfigInfo import config_info, content_info

configData = config_info()
headers = configData['headers']
prefix_url = configData['urls']['server_urls'][0] + configData['api_id']
send_url = configData['urls']['api_urls'][0]
set_callback = configData['urls']['api_urls'][1]
create_room = configData['urls']['api_urls'][2]
set_persistent = configData['urls']['api_urls'][4]
get_persistent = configData['urls']['api_urls'][5]
callback_server = configData['urls']['server_urls'][1]

bot_list = configData['bot_list']
single_bot = configData['single_bot']
single_account = config_info()['single_account']
message_count = configData['message_count']

member_list = configData['account_ids']

message_types = content_info()

"""

发送消息相关

"""


def send_single_message(accountId, msg_type, bot_num):
    """基本发送功能"""
    url = prefix_url + send_url
    params = {
        "botNo": bot_num,
        "accountId": accountId,
        "content": msg_type
    }
    response = requests.post(url, headers=headers, json=params)
    response_message = response.content.decode('utf-8')
    msg_dic = json.loads(response_message)
    print(msg_dic)
    if "errorMessage" in msg_dic:
        raise BadRequestError()


def send_all_type(accountId, bot_num):
    """一次发送所有类型的消息"""
    for i in range(len(message_types)):
        send_single_message(accountId, message_types[i], bot_num)


def send_one_type(accountId, bot_num, messageCount=message_count):
    """连续发送同一类型的消息"""
    typeNum = random.randint(0, len(message_types) - 1)
    for i in range(messageCount):
        send_single_message(accountId, message_types[typeNum], bot_num)


def send_complex(accountId, bot_num, messageCount=message_count):
    """连续多次发送不同类型的消息"""
    for i in range(messageCount):
        typeNum = random.randint(0, len(message_types) - 1)
        send_single_message(accountId, message_types[typeNum], bot_num)


"""

创建聊天室相关

"""


def chat_room(title):
    """创建有bot的聊天室"""
    url = prefix_url + create_room
    params = {
        "botNo": single_bot,
        "accountIdList": member_list,
        "title": title
    }
    response = requests.post(url, headers=headers, json=params)
    room_id = json.loads(response.content.decode('utf-8'))['roomId']
    return room_id


def send_message_in_room(roomId):
    """在bot聊天室中发送消息"""
    url = prefix_url + send_url
    params = {
        "botNo": single_bot,
        "roomId": roomId,
        "content": message_types[0]
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.content)


"""

callback服务器相关

"""


def bind_url(bot_num):
    """给bot注册callback地址"""
    url = prefix_url + set_callback
    params = {
        'botNo': bot_num,
        'callbackUrl': callback_server,
        'callbackEventList': ["text", "location", "sticker", "image"]
    }
    requests.post(url, headers=headers, json=params)


def bind_multiple_bot():
    """绑定多个bot到一个callback_url"""
    for bot_num in bot_list:
        bind_url(bot_num)


def bind_single_bot():
    """绑定一个bot到一个callback_url"""
    bind_url(single_bot)


def get_user_info(userData):
    """"解析客户端发送的消息"""
    json_data = json.loads(userData.split('\r\n')[-1])
    source_data = json_data['source']
    print(source_data)
    if 'roomId' in source_data:  # 如果用户在聊天室中发送消息，bot只在聊天室中进行回复
        return json_data['source']['roomId']
    else:
        return json_data['source']['accountId']


def multiple_callback(account_id):
    """调用多个bot回复"""
    for bot in bot_list:
        send_single_message(account_id, message_types[0], bot)


def single_callback(account_id):
    """使用一个bot回复"""
    send_single_message(account_id, message_types[0], single_bot)


def set_persistent_menu():
    """add persistent menu"""
    url = prefix_url + set_persistent
    params = {
        'botNo': 621,
        'content': {
            'buttons': [{
                'text': 'worksmobile\'s homepage',
                'link': 'https://line.worksmobile.com'
            }, {
                'text': 'FAQ',
                'postback': 'PersistentMenu_FAQ'
            }]
        }
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.content.decode('utf-8'))


def get_persistent_menu():
    """获取预设bot消息的内容"""
    url = prefix_url + get_persistent
    params = {
        'botNo': 621
    }
    response = requests.post(url, headers=headers, json=params)
    print(response.content)


"""

定义异常类

"""


class WrongBotNumError(Exception):  # 定义错误bot的异常
    def __init__(self):
        super().__init__()


class BadRequestError(Exception):
    def __init__(self):
        super().__init__()
        print('wrong bot num or accountId')


class NoSuchAccountIdError(Exception):  # 定义无效用户ID的异常
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    # send_single_message('johnny001@nwetest.com',message_types[3],single_bot)
    # set_persistent_menu()
    get_persistent_menu()
