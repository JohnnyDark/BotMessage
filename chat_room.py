from bot.all_methods import *

from messagebot.all_methods import chat_room, send_message_in_room


def invite_to_chatroom():

    """创建聊天室并在聊天室中发送消息"""
    room_name = input('please input the room name: ')
    room_id = chat_room(room_name)
    send_message_in_room(room_id)


if __name__ == '__main__':
    invite_to_chatroom()

