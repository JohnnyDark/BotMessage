from socket import AF_INET, socket, SOCK_STREAM

from all_methods import *


def receive_server():
    """本地建立消息接受服务端"""
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", 8888))
    server_socket.listen(10)
    bind_multiple_bot()
    while True:
        replay_message_type = eval(input('please input the way of callback: '))
        if replay_message_type not in [1, 2, 3, 4]:
            continue
        while True:
            new_socket, client_info = server_socket.accept()
            callback_data = new_socket.recv(1024).decode('utf-8')
            print(callback_data)
            message_target = get_user_info(callback_data)
            if '@' in message_target:
                print("ok")
                print(message_target)
                if replay_message_type == 1:
                    send_all_type(message_target, single_bot)
                    break
                elif replay_message_type == 2:
                    send_one_type(message_target, single_bot)
                    break
                elif replay_message_type == 3:
                    send_complex(message_target, single_bot)
                    break
                elif replay_message_type == 4:
                    multiple_callback(message_target)
                    break
            else:
                send_message_in_room(message_target)
                break


if __name__ == '__main__':
    receive_server()
